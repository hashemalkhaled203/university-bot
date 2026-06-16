#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج الأوامر الإدارية
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import config
from database import db

# حالات المحادثة
AWAITING_SUBJECT, AWAITING_PROFESSOR, AWAITING_DAY, AWAITING_TIME, AWAITING_ROOM = range(5)

async def add_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """إضافة محاضرة (أداري فقط)"""
    user_id = update.effective_user.id
    
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text(config.MESSAGES['admin_only'])
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📚 **إضافة محاضرة جديدة**\n\n"
        "أدخل اسم المادة:",
        parse_mode="Markdown"
    )
    return AWAITING_SUBJECT

async def receive_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """استقبال اسم المادة"""
    context.user_data['subject'] = update.message.text
    await update.message.reply_text("👨‍🏫 أدخل اسم الأستاذ:")
    return AWAITING_PROFESSOR

async def receive_professor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """استقبال اسم الأستاذ"""
    context.user_data['professor'] = update.message.text
    await update.message.reply_text(
        "📅 أدخل يوم الأسبوع (saturday, sunday, monday, ...):")
    return AWAITING_DAY

async def receive_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """استقبال يوم الأسبوع"""
    context.user_data['day'] = update.message.text.lower()
    await update.message.reply_text(
        "⏰ أدخل وقت البداية والنهاية (مثال: 08:00-10:00):")
    return AWAITING_TIME

async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """استقبال الوقت"""
    times = update.message.text.split('-')
    context.user_data['start_time'] = times[0].strip()
    context.user_data['end_time'] = times[1].strip() if len(times) > 1 else "00:00"
    await update.message.reply_text("🏛️ أدخل رقم القاعة:")
    return AWAITING_ROOM

async def receive_room(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """استقبال رقم القاعة"""
    context.user_data['room'] = update.message.text
    
    # إضافة المحاضرة
    db.add_class(
        context.user_data['subject'],
        context.user_data['professor'],
        context.user_data['day'],
        context.user_data['start_time'],
        context.user_data['end_time'],
        context.user_data['room']
    )
    
    await update.message.reply_text(
        f"✅ تم إضافة المحاضرة بنجاح!\n\n"
        f"📚 {context.user_data['subject']}\n"
        f"👨‍🏫 {context.user_data['professor']}\n"
        f"📅 {context.user_data['day']}\n"
        f"⏰ {context.user_data['start_time']} - {context.user_data['end_time']}\n"
        f"🏛️ القاعة {context.user_data['room']}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def remove_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """حذف محاضرة (إداري فقط)"""
    user_id = update.effective_user.id
    
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text(config.MESSAGES['admin_only'])
        return
    
    await update.message.reply_text(
        "🗑️ **حذف محاضرة**\n\n"
        "هذه الميزة قيد التطوير...",
        parse_mode="Markdown"
    )
