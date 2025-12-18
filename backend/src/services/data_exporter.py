"""
Data Exporter Service
Exports heatmap data to JSON format with context summaries for AI analysis.
"""

import logging
from typing import Dict, List, Optional
import pandas as pd
from .data_loader import get_cache

logger = logging.getLogger(__name__)


class DataExporter:
    """
    Service for exporting filtered heatmap data to JSON format.

    Builds data context with summary statistics for AI chatbot analysis.
    """

    def __init__(self):
        """Initialize data exporter with access to data cache."""
        self.cache = get_cache()
        logger.info("DataExporter initialized")

    def export_to_json(
        self,
        month: int,
        hour: int,
        day_type: str
    ) -> List[Dict]:
        """
        Export filtered data as list of dictionaries.

        Args:
            month: Month identifier (YYYYMM format)
            hour: Hour of day (0-23)
            day_type: Day type ("平日" or "假日")

        Returns:
            List of data records as dictionaries with 23 fields
        """
        # Get filtered data from cache (O(1) lookup)
        filtered_df = self.cache.lookup_dict.get((month, hour, day_type))

        if filtered_df is None or filtered_df.empty:
            return []

        # Select required columns (23 fields from spec)
        required_cols = [
            'month', 'gx', 'gy', 'lat', 'lng', 'hour', 'day_type',
            'avg_total_users', 'avg_users_under_10min', 'avg_users_10_30min', 'avg_users_over_30min',
            'sex_1', 'sex_2',
            'age_1', 'age_2', 'age_3', 'age_4', 'age_5', 'age_6', 'age_7', 'age_8', 'age_9', 'age_other'
        ]

        # Note: 'lng' column might be 'lon' in some datasets, check and adapt
        if 'lng' not in filtered_df.columns and 'lon' in filtered_df.columns:
            filtered_df = filtered_df.rename(columns={'lon': 'lng'})

        # Convert to list of dicts
        data_records = filtered_df[required_cols].to_dict('records')

        # Convert numpy types to Python native types for JSON serialization
        for record in data_records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = 0.0 if isinstance(value, (int, float)) else None
                elif hasattr(value, 'item'):  # numpy types
                    record[key] = value.item()

        return data_records

    def get_context_summary(
        self,
        month: int,
        hour: int,
        day_type: str
    ) -> Dict:
        """
        Get summary statistics for current data context.

        Calculates aggregated metrics for AI prompt context including all metrics
        used in frontend visualizations.

        Args:
            month: Month identifier (YYYYMM format)
            hour: Hour of day (0-23)
            day_type: Day type ("平日" or "假日")

        Returns:
            Dictionary with comprehensive statistics including:
            - Basic stats: total_records, total_users
            - Duration stats: users by stay duration (<10min, 10-30min, >30min)
            - Gender stats: avg_sex_1 (male), avg_sex_2 (female)
            - Age distribution: age_1 to age_9, age_other
            - Top locations: top 5 locations by user count
        """
        # Get filtered data
        filtered_df = self.cache.lookup_dict.get((month, hour, day_type))

        if filtered_df is None or filtered_df.empty:
            return {
                'total_records': 0,
                'total_users': 0.0,
                'duration_distribution': {
                    'under_10min': 0.0,
                    'min_10_30': 0.0,
                    'over_30min': 0.0
                },
                'gender_distribution': {
                    'male_pct': 0.0,
                    'female_pct': 0.0
                },
                'age_distribution': {
                    'age_1': 0.0, 'age_2': 0.0, 'age_3': 0.0, 'age_4': 0.0, 'age_5': 0.0,
                    'age_6': 0.0, 'age_7': 0.0, 'age_8': 0.0, 'age_9': 0.0, 'age_other': 0.0
                },
                'top_locations': []
            }

        # Handle lng/lon column name
        lng_col = 'lng' if 'lng' in filtered_df.columns else 'lon'

        # Calculate summary statistics
        total_records = len(filtered_df)
        total_users = float(filtered_df['avg_total_users'].sum())

        # Duration distribution (actual user counts, not percentages)
        total_under_10min = float(filtered_df['avg_users_under_10min'].sum()) if 'avg_users_under_10min' in filtered_df.columns else 0.0
        total_10_30min = float(filtered_df['avg_users_10_30min'].sum()) if 'avg_users_10_30min' in filtered_df.columns else 0.0
        total_over_30min = float(filtered_df['avg_users_over_30min'].sum()) if 'avg_users_over_30min' in filtered_df.columns else 0.0

        # Weighted average demographics (percentages)
        weights = filtered_df['avg_total_users'].values
        if total_users > 0:
            avg_sex_1 = float((filtered_df['sex_1'] * weights).sum() / total_users)
            avg_sex_2 = float((filtered_df['sex_2'] * weights).sum() / total_users)
        else:
            avg_sex_1 = 0.0
            avg_sex_2 = 0.0

        # Age distribution (weighted percentages)
        age_distribution = {}
        for i in range(1, 10):
            col = f'age_{i}'
            if col in filtered_df.columns and total_users > 0:
                age_distribution[col] = float((filtered_df[col] * weights).sum() / total_users)
            else:
                age_distribution[col] = 0.0

        if 'age_other' in filtered_df.columns and total_users > 0:
            age_distribution['age_other'] = float((filtered_df['age_other'] * weights).sum() / total_users)
        else:
            age_distribution['age_other'] = 0.0

        # Top 5 locations by total users
        top_5 = filtered_df.nlargest(5, 'avg_total_users')
        top_locations = []
        for _, row in top_5.iterrows():
            top_locations.append({
                'lat': float(row['lat']),
                'lon': float(row[lng_col]),
                'total_users': float(row['avg_total_users']),
                'under_10min': float(row.get('avg_users_under_10min', 0)),
                '10_30min': float(row.get('avg_users_10_30min', 0)),
                'over_30min': float(row.get('avg_users_over_30min', 0))
            })

        return {
            'total_records': total_records,
            'total_users': total_users,
            'duration_distribution': {
                'under_10min': total_under_10min,
                'min_10_30': total_10_30min,
                'over_30min': total_over_30min
            },
            'gender_distribution': {
                'male_pct': avg_sex_1,
                'female_pct': avg_sex_2
            },
            'age_distribution': age_distribution,
            'top_locations': top_locations
        }


# Global exporter instance
_data_exporter: Optional[DataExporter] = None


def get_data_exporter() -> DataExporter:
    """Get or create the global data exporter instance."""
    global _data_exporter
    if _data_exporter is None:
        _data_exporter = DataExporter()
    return _data_exporter
