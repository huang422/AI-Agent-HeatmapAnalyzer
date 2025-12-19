# Docker Deployment Guide

這份文件說明如何使用 Docker 部署 Store Heatmap 應用程式，並透過 ngrok 讓外網使用者訪問。

## 概述

此 Docker 配置包含三個服務：
- **Backend**: FastAPI 應用程式 (Port 8000)
- **Frontend**: Nginx 提供的 Vue.js 應用程式 (Port 80)
- **Ngrok**: 將應用程式暴露到公網的隧道服務

## 前置需求

1. **Docker** (版本 20.10 或以上)
   - 下載: https://docs.docker.com/get-docker/

2. **Docker Compose** (版本 2.0 或以上)
   - 通常隨 Docker Desktop 一起安裝
   - Linux 使用者: https://docs.docker.com/compose/install/

3. **數據檔案**
   - 確保 `./data/data.csv` 存在

## 快速開始

### 1. 基本啟動

最簡單的方式是使用提供的啟動腳本：

```bash
./start-docker.sh
```

腳本會自動：
- 檢查 Docker 是否安裝
- 建置並啟動所有服務
- 等待服務就緒
- 顯示本地和公網訪問網址
- 顯示 ngrok 公網 URL

### 2. 手動啟動

如果想手動控制，可以使用以下指令：

```bash
# 建置並啟動所有服務
docker compose up -d --build

# 查看服務狀態
docker compose ps

# 查看日誌
docker compose logs -f

# 停止所有服務
docker compose down
```

## 訪問應用程式

### 本地訪問

啟動後，可以透過以下網址訪問：

- **前端應用**: http://localhost
- **後端 API**: http://localhost:8000
- **API 文檔**: http://localhost:8000/docs
- **Ngrok Dashboard**: http://localhost:4040

### 公網訪問 (透過 Ngrok)

Ngrok 會自動建立一個公網隧道。獲取公網 URL 的方式：

1. **自動顯示**: 啟動腳本會自動顯示公網 URL

2. **手動查詢**: 訪問 http://localhost:4040 查看 Ngrok Dashboard

3. **API 查詢**:
   ```bash
   curl http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*'
   ```

公網 URL 格式類似: `https://xxxx-xxx-xxx-xxx.ngrok-free.app`

將此 URL 分享給任何人，他們就能訪問你的應用程式！

## Ngrok 進階配置

### 使用 Ngrok Authtoken (推薦)

免費的 ngrok 隧道會在 2 小時後斷開。使用 authtoken 可以獲得更穩定的服務：

1. 註冊 ngrok 帳號: https://dashboard.ngrok.com/signup

2. 獲取 authtoken: https://dashboard.ngrok.com/get-started/your-authtoken

3. 建立 `.env` 檔案：
   ```bash
   cp .env.example .env
   ```

4. 編輯 `.env`，加入你的 authtoken：
   ```env
   NGROK_AUTHTOKEN=your_actual_authtoken_here
   ```

5. 重新啟動服務：
   ```bash
   docker compose down
   docker compose up -d
   ```

### 使用自訂網域 (需付費方案)

如果你有 ngrok 付費方案，可以使用自訂網域：

1. 在 `.env` 中設定：
   ```env
   NGROK_AUTHTOKEN=your_authtoken
   NGROK_DOMAIN=your-custom-domain.ngrok.app
   ```

2. 取消 `docker-compose.yml` 中的註解：
   ```yaml
   environment:
     - NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}
     - NGROK_DOMAIN=${NGROK_DOMAIN}
   ```

### 選擇 Ngrok 區域

根據你的地理位置選擇最近的 ngrok 伺服器以獲得最佳效能：

在 `.env` 中設定：
```env
NGROK_REGION=ap  # 亞太地區
```

可用區域：
- `us` - 美國 (預設)
- `eu` - 歐洲
- `ap` - 亞太
- `au` - 澳洲
- `sa` - 南美
- `jp` - 日本
- `in` - 印度

## 常用指令

### 查看服務狀態
```bash
docker compose ps
```

### 查看即時日誌
```bash
# 所有服務
docker compose logs -f

# 特定服務
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f ngrok
```

### 重新啟動服務
```bash
# 重啟所有服務
docker compose restart

# 重啟特定服務
docker compose restart backend
```

### 停止服務
```bash
# 停止但保留容器
docker compose stop

# 停止並移除容器
docker compose down

# 停止並移除容器及映像
docker compose down --rmi all
```

### 重新建置
```bash
# 重新建置並啟動
docker compose up -d --build

# 只建置特定服務
docker compose build backend
```

### 進入容器
```bash
# 進入 backend 容器
docker exec -it store-heatmap-backend bash

# 進入 frontend 容器
docker exec -it store-heatmap-frontend sh
```

## 架構說明

### Docker 網路

所有服務在同一個 bridge 網路 `heatmap-network` 中運行，可以透過服務名稱互相通訊：

- Backend 可以透過 `http://backend:8000` 訪問
- Frontend 可以透過 `http://frontend:80` 訪問

### 資料卷掛載

- `./data:/app/data:ro` - 數據目錄 (唯讀)
- `./backend/src:/app/src` - 開發模式下的熱重載 (可選)

### 健康檢查

所有服務都配置了健康檢查：
- **Backend**: 每 30 秒檢查 `/health` 端點
- **Frontend**: 每 30 秒檢查根路徑
- 服務依賴會等待健康檢查通過後才啟動

## 故障排除

### 服務無法啟動

1. 檢查日誌：
   ```bash
   docker compose logs backend
   docker compose logs frontend
   ```

2. 確認 port 沒有被佔用：
   ```bash
   # Linux/Mac
   lsof -i :80
   lsof -i :8000

   # Windows
   netstat -ano | findstr :80
   netstat -ano | findstr :8000
   ```

### Ngrok 無法取得 URL

1. 檢查 ngrok 服務狀態：
   ```bash
   docker compose logs ngrok
   ```

2. 訪問 ngrok dashboard: http://localhost:4040

3. 確認是否需要設定 authtoken

### 資料無法載入

1. 確認 `./data/data.csv` 存在且格式正確

2. 檢查檔案權限：
   ```bash
   ls -la ./data/data.csv
   ```

3. 查看 backend 日誌：
   ```bash
   docker compose logs backend
   ```

### Frontend 無法連接到 Backend

1. 檢查 nginx 配置中的 proxy_pass 設定
2. 確認 backend 服務正在運行：
   ```bash
   docker compose ps backend
   ```

## 安全性注意事項

1. **生產環境**: 此配置主要用於開發和測試。生產環境應考慮：
   - 移除開發用的 volume 掛載
   - 使用環境變數管理敏感資訊
   - 加入 SSL/TLS 配置
   - 設定適當的 CORS 政策

2. **Ngrok 限制**:
   - 免費版每個 URL 2 小時會話限制
   - 公網 URL 是公開的，任何人都能訪問
   - 建議在測試完成後關閉服務

3. **資料隱私**:
   - 確認分享的資料不包含敏感資訊
   - 考慮加入認證機制

## 效能優化

### 生產模式建置

編輯 `docker-compose.yml`，移除開發用的 volume：

```yaml
backend:
  volumes:
    - ./data:/app/data:ro
    # 移除這行: - ./backend/src:/app/src
```

### 記憶體限制

加入資源限制：

```yaml
backend:
  deploy:
    resources:
      limits:
        memory: 512M
      reservations:
        memory: 256M
```
# Docker 快速指令參考

## 啟動服務
```bash
./start-docker.sh              # 自動啟動所有服務(推薦)
docker compose up -d           # 手動啟動所有服務
docker compose up              # 啟動並顯示日誌
```

## 停止服務
```bash
docker compose stop            # 停止(保留容器)
docker compose down            # 停止並移除容器
docker compose down --rmi all  # 停止並移除容器+映像檔
sudo docker compose down && sudo docker compose up -d 
```

## 重啟服務
```bash
docker compose restart         # 重啟所有服務
docker compose restart backend # 重啟特定服務
```

## 查看狀態
```bash
docker compose ps              # 查看容器狀態
docker compose logs -f         # 查看即時日誌
docker compose logs -f backend # 查看特定服務日誌
```

## 重建服務
```bash
docker compose up -d --build           # 重建所有服務
docker compose up -d --build backend   # 重建特定服務
docker compose build --no-cache        # 清除快取重建
```

## Ngrok 相關
```bash
# 查看公網網址
curl http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*'

# 訪問控制台
# http://localhost:4040
```

## 訪問網址
- Frontend:        http://localhost
- Backend API:     http://localhost:8000
- API Docs:        http://localhost:8000/docs
- Ngrok Dashboard: http://localhost:4040

## 常見操作

### 修改 Backend 程式碼
```bash
# 有熱重載,只需重啟
docker compose restart backend
```

### 修改 Frontend 程式碼
```bash
# 需要重建
docker compose up -d --build frontend
```

### 完全重置
```bash
docker compose down --rmi all
./start-docker.sh
```

### 進入容器除錯
```bash
docker exec -it store-heatmap-backend bash
docker exec -it store-heatmap-frontend sh
```

echo "========================================="
echo "步驟 1: 停止並清除所有 Docker 資源"
echo "========================================="
sudo docker compose down --rmi all --volumes

echo -e "\n========================================="
echo "步驟 2: 清除 Docker 建置快取"
echo "========================================="
sudo docker builder prune -af

echo -e "\n========================================="
echo "步驟 3: 重新建置 (不使用快取)"
echo "========================================="
sudo docker compose build --no-cache

echo -e "\n========================================="
echo "步驟 4: 啟動所有服務"
echo "========================================="
sudo docker compose up -d

echo -e "\n========================================="
echo "步驟 5: 等待服務啟動"
echo "========================================="
sleep 10

echo -e "\n========================================="
echo "步驟 6: 檢查容器狀態"
echo "========================================="
sudo docker compose ps

echo -e "\n========================================="
echo "步驟 7: 檢查 Backend 日誌"
echo "========================================="
sudo docker compose logs backend --tail=20

echo -e "\n========================================="
echo "步驟 8: 測試訪問"
echo "========================================="
echo "Frontend 狀態:"
curl -s -o /dev/null -w 'HTTP %{http_code}\n' http://localhost

echo "Backend 狀態:"
curl -s http://localhost:8000/health

echo -e "\n========================================="
echo "步驟 9: 獲取 Ngrok 公網網址"
echo "========================================="
sleep 3
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1

echo -e "\n========================================="
echo "✅ Docker 重建完成!"
echo "========================================="
echo "本地訪問: http://localhost"
echo "API 文檔: http://localhost:8000/docs"
echo "Ngrok 控制台: http://localhost:4040"
echo "========================================="

## 支援

如有問題，請聯繫：
- Tom Huang
- Email: huang1473690@gmail.com

