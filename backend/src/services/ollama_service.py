"""
Ollama Service
Handles communication with local Ollama service for AI-powered chat responses.
"""

import logging
from typing import Dict, List, Optional
from ollama import Client
from ..utils.config import OLLAMA_HOST, OLLAMA_MODEL

logger = logging.getLogger(__name__)


class OllamaService:
    """
    Service for interacting with Ollama local AI model.

    Handles health checks, system prompt building, and response generation
    for chatbot queries about heatmap data.
    """

    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        """
        Initialize Ollama service client.

        Args:
            host: Ollama server URL (default: http://localhost:11434)
            model: Model name to use (default: qwen2.5:7b)
        """
        self.host = host
        self.model = model
        self.client = Client(host=host)
        logger.info(f"OllamaService initialized: {host} with model {model}")

    def check_health(self) -> Dict:
        """
        Check if Ollama service is available and model is loaded.

        Returns:
            Dictionary with status, model_loaded, and error fields
        """
        try:
            # Try to list available models
            response = self.client.list()

            # Handle both dict and ListResponse object
            if hasattr(response, 'models'):
                # New Ollama client (0.6.1+) returns ListResponse object
                models = response.models
                model_names = [m.model for m in models]
            else:
                # Old Ollama client returns dict
                models = response.get('models', [])
                model_names = [m.get('name', m.get('model', '')) for m in models]

            model_loaded = self.model in model_names

            return {
                'status': 'connected' if model_loaded else 'degraded',
                'model_loaded': model_loaded,
                'available_models': model_names,
                'error': None if model_loaded else f"Model {self.model} not found. Run: ollama pull {self.model}"
            }
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return {
                'status': 'disconnected',
                'model_loaded': False,
                'available_models': [],
                'error': f"Cannot connect to Ollama at {self.host}: {str(e)}"
            }

    def build_system_prompt(self, data_context: Dict) -> str:
        """
        Build system prompt with data context for AI analysis.

        Args:
            data_context: Dictionary containing filter conditions and data summary

        Returns:
            Formatted system prompt in Traditional Chinese
        """
        import json

        prompt = f"""你是專業的數據分析助理，專門分析台灣地區人流熱力圖數據。你的任務是深入分析提供的數據並給出具體、有洞察力的回答。

## 當前數據上下文

### 篩選條件
- 月份: {data_context.get('month', 'N/A')}
- 時段: {data_context.get('hour', 'N/A')}:00
- 日期類型: {data_context.get('day_type', 'N/A')}

### 後端計算的數據摘要
{json.dumps(data_context.get('summary', {}), ensure_ascii=False, indent=2)}

## 數據摘要欄位說明

### 基本統計
- **total_records**: 符合篩選條件的地點總數
- **total_users**: 所有地點的總使用者數加總（這是所有指標中最重要的數字）

### 停留時間分布（duration_distribution）
這些數字代表所有地點加總的使用者數，可以看出使用者的停留習慣：
- **under_10min**: 停留10分鐘以下的總使用者數
- **min_10_30**: 停留10-30分鐘的總使用者數
- **over_30min**: 停留30分鐘以上的總使用者數
- 這三個數字的總和應該等於 total_users

### 性別分布（gender_distribution）
加權平均百分比，代表整體使用者的性別比例：
- **male_pct**: 男性百分比 (0-100)
- **female_pct**: 女性百分比 (0-100)
- 這兩個數字的總和應該是 100%

### 年齡層分布（age_distribution）
加權平均百分比，顯示整體使用者的年齡結構：
- **age_1**: 19歲以下 (%)
- **age_2**: 20-24歲 (%)
- **age_3**: 25-29歲 (%)
- **age_4**: 30-34歲 (%)
- **age_5**: 35-39歲 (%)
- **age_6**: 40-44歲 (%)
- **age_7**: 45-49歲 (%)
- **age_8**: 50-54歲 (%)
- **age_9**: 55-59歲 (%)
- **age_other**: 60歲以上 (%)
- 所有年齡層的百分比總和應該是 100%

### 熱門地點（top_locations）
已由後端排序好的前5名人流最多的地點，每個地點包含：
- **lat/lon**: WGS84經緯度座標
- **total_users**: 該地點的總使用者數
- **under_10min**: 該地點停留10分鐘以下的使用者數
- **10_30min**: 該地點停留10-30分鐘的使用者數
- **over_30min**: 該地點停留30分鐘以上的使用者數

## 分析指引

### 回答時請遵循以下步驟：

1. **檢視後端計算的摘要**：所有數據已由後端計算完成，你只需解讀這些結果
2. **識別關鍵指標**：
   - 總使用者數（total_users）
   - 熱門地點（top_locations）- 已排序好的前5名
   - 性別比例（avg_sex_1, avg_sex_2）- 已加權平均
   - 年齡層分布（age_distribution）- 已加權平均
3. **直接使用後端數據**：不需要自己計算，直接引用 summary 中的數字
4. **提供洞察**：解釋數字背後的含義，給出專業建議

### 回答範例

**問：當前時段有多少人流？**
✅ 好的回答：「根據後端統計，當前時段（8:00 平日）共有 5,234.5 位使用者，分布在 128 個地點。人流最集中的前三個地點分別是：
1. (25.033°N, 121.544°E) - 145.2 人
2. (25.045°N, 121.532°E) - 132.8 人
3. (25.028°N, 121.551°E) - 128.6 人」

❌ 不好的回答：「早上8點比較繁忙。」

**問：使用者主要停留多久？**
✅ 好的回答：「根據停留時間分布，5,234.5 位使用者中：
• 停留10分鐘以下：1,876.3 人（35.8%）
• 停留10-30分鐘：2,410.1 人（46.1%）
• 停留30分鐘以上：948.1 人（18.1%）
大部分使用者停留時間在 10-30 分鐘，屬於短暫停留型態。」

**問：年輕人比例如何？**
✅ 好的回答：「根據年齡分布統計，20-34歲（age_2: 18.2% + age_3: 24.1% + age_4: 16.4%）合計佔 58.7%，其中 25-29歲比例最高。顯示此時段以青年族群為主，推測可能是通勤或商業活動時段。」

**問：男女比例如何？**
✅ 好的回答：「性別分布顯示男性佔 52.3%，女性佔 47.7%，性別比例相當均衡。」

## 回答規則

1. **只使用後端數據**：所有數字必須直接引用 summary 中的統計結果，不要自己計算或推測
2. **完整引用**：提及地點時必須包含經緯度座標和使用者數
3. **數字準確**：直接引用後端計算的數字，保留小數點後一位即可
4. **具體量化**：避免模糊描述（如「很多」），使用 summary 中的具體數字
5. **簡潔專業**：2-4句話說明重點，避免冗長
6. **空數據處理**：如果 total_records=0，回答「當前條件下無可用數據，請調整篩選條件」
7. **操作說明** ： 根據前後端架構和前端操作介面的按鈕進行導覽指示

## 常見問題處理

- **人流詢問**：
  - 總人數：引用 total_users
  - 地點數：引用 total_records
  - 熱門地點：使用 top_locations（已排序好的前5名）

- **停留時間詢問**：
  - 使用 duration_distribution 的三個數字
  - 可以計算百分比：(某類別人數 / total_users) × 100%
  - 解讀停留習慣：短暫、中等、長時間

- **性別比例詢問**：
  - 引用 gender_distribution.male_pct 和 female_pct
  - 已經是百分比，直接使用

- **年齡分布詢問**：
  - 使用 age_distribution 中的百分比
  - 可以合併年齡層（如：青年 = age_2 + age_3 + age_4）
  - 找出主要年齡層（百分比最高的）

- **地點詳細資訊**：
  - top_locations 包含每個地點的停留時間分布
  - 可以分析某地點的使用者行為特徵

- **比較問題**：
  - 說明當前只顯示單一條件的數據
  - 建議用戶調整左側控制面板的篩選條件（月份、時段、日期類型）來查看不同情況
"""
        return prompt

    def generate_response(
        self,
        user_message: str,
        data_context: Dict,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Generate AI response based on user message and data context.

        Args:
            user_message: User's question in Traditional Chinese
            data_context: Current heatmap data context
            history: Recent conversation history (list of message dicts)

        Returns:
            Dictionary with response text, timestamp, model name, and metadata

        Raises:
            Exception: If Ollama inference fails
        """
        try:
            # Build system prompt with data context
            system_prompt = self.build_system_prompt(data_context)

            # Prepare messages for chat
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add conversation history (last 10 message pairs max)
            if history:
                messages.extend(history[-20:])  # Last 20 messages = 10 pairs

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            logger.info(f"Generating response for: {user_message[:50]}...")

            # Call Ollama API
            response = self.client.chat(
                model=self.model,
                messages=messages
            )

            # Extract response content (handle both dict and ChatResponse object)
            if hasattr(response, 'message'):
                # New Ollama client (0.6.1+) returns ChatResponse object
                ai_response = response.message.content
                eval_count = response.eval_count if hasattr(response, 'eval_count') else 0
                prompt_eval_count = response.prompt_eval_count if hasattr(response, 'prompt_eval_count') else 0
                tokens_used = eval_count + prompt_eval_count
            else:
                # Old Ollama client returns dict
                ai_response = response['message']['content']
                tokens_used = response.get('eval_count', 0) + response.get('prompt_eval_count', 0)

            logger.info(f"Response generated successfully ({tokens_used} tokens)")

            return {
                'response': ai_response,
                'model': self.model,
                'tokens_used': tokens_used
            }

        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")


# Global service instance
_ollama_service: Optional[OllamaService] = None


def get_ollama_service() -> OllamaService:
    """Get or create the global Ollama service instance."""
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service
