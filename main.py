#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 University Bot - بوت الجامعة المتكامل
Author: @hashem_alkhaled203
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import config
from handlers import start, schedule, reminders, quiz, admin, membership

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """بدء البوت"""
    # إنشاء التطبيق
    application = Application.builder().token(config.TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start.start_command))
    application.add_handler(CommandHandler("help", start.help_command))
    
    # معالجات الجدول الدراسي
    application.add_handler(CommandHandler("schedule", schedule.show_schedule))
    application.add_handler(CommandHandler("add_class", admin.add_class))
    application.add_handler(CommandHandler("remove_class", admin.remove_class))
    
    # معالجات التذكيرات
    application.add_handler(CommandHandler("reminders", reminders.manage_reminders))
    
    # معالجات المسابقات
    application.add_handler(CommandHandler("quiz", quiz.start_quiz))
    
    # معالج الأزرار
    application.add_handler(CallbackQueryHandler(start.button_callback))
    
    # معالج فحص العضوية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, membership.check_membership))
    
    # بدء التطبيق
    logger.info("🚀 البوت بدأ التشغيل...")
    application.run_polling()

if __name__ == '__main__':
    main()
