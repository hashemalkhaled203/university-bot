#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج المسابقات
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import db

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """بدء مسابقة"""
    await update.message.reply_text(
        "📝 **المسابقات**\n\n"
        "اختر مادة لبدء المسابقة:\n\n"
        "/quiz_math - رياضيات\n"
        "/quiz_physics - فيزياء\n"
        "/quiz_programming - البرمجة\n",
        parse_mode="Markdown"
    )
