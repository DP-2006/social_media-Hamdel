import joblib
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from ..models import MLModelRegistry, PredictionCache

class BaseMLService:
    """کلاس پایه برای همه سرویس‌های ML"""
    
    def __init__(self, model_type, model_name=None):
        self.model_type = model_type
        self.model_name = model_name or f"{model_type}_model"
        self.model = None
        self.version = None
        self.metadata = {}
        self._load_model()
    
    def _load_model(self):
        """بارگذاری آخرین نسخه فعال مدل"""
        try:
            latest_model = MLModelRegistry.objects.filter(
                model_type=self.model_type,
                status='active'
            ).first()
            
            if latest_model and latest_model.model_path:
                model_path = Path(settings.ML_MODELS_DIR) / latest_model.model_path
                if model_path.exists():
                    self.model = joblib.load(model_path)
                    self.version = latest_model.version
                    self.metadata = latest_model.metadata
                    return True
        except Exception as e:
            print(f"Error loading model {self.model_type}: {e}")
        
        return False
    
    def predict(self, input_data):
        """پیش‌بینی با کشینگ هوشمند"""
        # تولید کلید کش
        cache_key = self._generate_cache_key(input_data)
        
        # بررسی کش دیتابیس
        cached = PredictionCache.objects.filter(
            cache_key=cache_key,
            expires_at__gt=datetime.now()
        ).first()
        
        if cached:
            cached.hit_count += 1
            cached.save()
            return cached.prediction_result
        
        # پیش‌بینی واقعی
        result = self._predict_impl(input_data)
        
        # ذخیره در کش
        PredictionCache.objects.create(
            cache_key=cache_key,
            model_type=self.model_type,
            input_hash=hashlib.md5(json.dumps(input_data).encode()).hexdigest(),
            prediction_result=result,
            confidence=result.get('confidence', 0.0),
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        return result
    
    def _generate_cache_key(self, input_data):
        """تولید کلید یکتا برای کش"""
        data_str = json.dumps(input_data, sort_keys=True)
        hash_input = f"{self.model_type}:{self.version}:{data_str}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _predict_impl(self, input_data):
        """پیاده‌سازی واقعی پیش‌بینی (باید در کلاس فرزند override شود)"""
        raise NotImplementedError
    
    def get_health_status(self):
        """وضعیت سلامت سرویس"""
        return {
            'model_type': self.model_type,
            'is_loaded': self.model is not None,
            'version': self.version,
            'metadata': self.metadata
        }