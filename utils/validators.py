#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أدوات التحقق من البيانات
"""

import re
from typing import Tuple

def validate_time_format(time_str: str) -> bool:
    """التحقق من صيغة الوقت (HH:MM)"""
    pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def validate_gpa(gpa: float) -> bool:
    """التحقق من صحة المعدل"""
    return 0.0 <= gpa <= 4.0

def parse_time_range(time_range: str) -> Tuple[str, str]:
    """تحليل نطاق الوقت"""
    times = time_range.split('-')
    if len(times) == 2:
        return times[0].strip(), times[1].strip()
    return None, None
