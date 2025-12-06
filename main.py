#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易答题软件
支持单选题、多选题、题目导入等功能
"""

import sys
import json
import os
import re
from pathlib import Path
from openpyxl import load_workbook
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QRadioButton, QCheckBox, QButtonGroup,
    QFileDialog, QMessageBox, QScrollArea, QFrame, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette


class QuestionWidget(QWidget):
    """单个题目显示组件"""
    
    def __init__(self, question_data, parent=None):
        super().__init__(parent)
        self.question_data = question_data
        self.is_multiple = question_data.get('type') == 'multiple'
        self.selected_answers = []
        self.option_frames = []
        self.option_labels = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 统一的题目容器（包含题目和选项）
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        main_layout_inner = QVBoxLayout()
        main_layout_inner.setSpacing(0)
        main_layout_inner.setContentsMargins(0, 0, 0, 0)
        
        # 顶部装饰条和题目类型标签
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #42A5F5);
                border-radius: 12px 12px 0px 0px;
                padding: 15px 20px;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        # 题目类型标签
        type_label = QLabel("【单选题】" if not self.is_multiple else "【多选题】")
        type_label.setStyleSheet("""
            color: white;
            font-weight: 600;
            font-size: 13px;
            padding: 6px 14px;
            background-color: rgba(255, 255, 255, 0.25);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)
        header_layout.addWidget(type_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        main_layout_inner.addWidget(header_frame)
        
        # 题目内容区域
        question_frame = QFrame()
        question_frame.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                padding: 30px 25px;
            }
        """)
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(0, 0, 0, 0)
        question_layout.setSpacing(0)
        
        question_label = QLabel(self.question_data.get('question', ''))
        question_label.setWordWrap(True)
        question_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #212121;
            line-height: 1.8;
            padding: 0px;
        """)
        question_layout.addWidget(question_label)
        question_frame.setLayout(question_layout)
        main_layout_inner.addWidget(question_frame)
        
        # 选项容器
        options_frame = QFrame()
        options_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                padding: 20px 25px 30px 25px;
                border-radius: 0px 0px 12px 12px;
            }
        """)
        options_layout = QVBoxLayout()
        options_layout.setSpacing(14)
        options_layout.setContentsMargins(0, 0, 0, 0)
        
        self.button_group = QButtonGroup(self)
        self.option_buttons = []
        self.option_frames = []  # 存储选项框架，用于显示答案
        self.option_labels = []  # 存储选项标签
        
        options = self.question_data.get('options', [])
        for i, option in enumerate(options):
            # 创建选项容器
            option_frame = QFrame()
            option_frame.setStyleSheet("""
                QFrame {
                    background-color: #F8F9FA;
                    border: 2px solid #E0E0E0;
                    border-radius: 10px;
                    padding: 0px;
                }
                QFrame:hover {
                    background-color: #F0F4F8;
                    border-color: #2196F3;
                    border-width: 2px;
                }
            """)
            option_layout = QHBoxLayout()
            option_layout.setContentsMargins(18, 16, 18, 16)
            option_layout.setSpacing(15)
            
            if self.is_multiple:
                checkbox = QCheckBox()
                checkbox.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 22px;
                        height: 22px;
                        border: 2px solid #757575;
                        border-radius: 4px;
                        background-color: white;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #2196F3;
                        border-color: #2196F3;
                    }
                    QCheckBox::indicator:checked::after {
                        content: "✓";
                        color: white;
                    }
                """)
                # 使用闭包正确捕获索引
                def make_handler(idx):
                    return lambda checked: self.on_option_changed(idx, Qt.Checked if checked else Qt.Unchecked)
                checkbox.toggled.connect(make_handler(i))
                option_layout.addWidget(checkbox)
                self.option_buttons.append(checkbox)
            else:
                radio = QRadioButton()
                radio.setStyleSheet("""
                    QRadioButton::indicator {
                        width: 22px;
                        height: 22px;
                        border: 2px solid #757575;
                        border-radius: 11px;
                        background-color: white;
                    }
                    QRadioButton::indicator:checked {
                        background-color: #2196F3;
                        border-color: #2196F3;
                    }
                """)
                self.button_group.addButton(radio, i)
                option_layout.addWidget(radio)
                self.option_buttons.append(radio)
            
            # 选项标签
            option_label = QLabel(f"<span style='font-size: 16px; font-weight: 600; color: #1976D2;'>{chr(65 + i)}.</span> <span style='font-size: 15px; color: #424242;'>{option}</span>")
            option_label.setStyleSheet("""
                padding: 0px;
                background-color: transparent;
                border: none;
            """)
            option_label.setWordWrap(True)
            option_layout.addWidget(option_label, 1)
            option_frame.setLayout(option_layout)
            options_layout.addWidget(option_frame)
            
            # 保存引用
            self.option_frames.append(option_frame)
            self.option_labels.append(option_label)
        
        options_frame.setLayout(options_layout)
        main_layout_inner.addWidget(options_frame)
        main_frame.setLayout(main_layout_inner)
        layout.addWidget(main_frame)
        
        self.setLayout(layout)
    
    def on_option_changed(self, index, state):
        """多选题选项变化处理"""
        if state == Qt.Checked:
            if index not in self.selected_answers:
                self.selected_answers.append(index)
        else:
            if index in self.selected_answers:
                self.selected_answers.remove(index)
    
    def get_selected_answers(self):
        """获取选中的答案"""
        if self.is_multiple:
            # 多选题：直接从复选框状态获取，确保准确性
            selected = []
            for i, checkbox in enumerate(self.option_buttons):
                if checkbox.isChecked():
                    selected.append(i)
            return sorted(selected)
        else:
            # 单选题：从单选按钮获取
            for i, button in enumerate(self.option_buttons):
                if button.isChecked():
                    return [i]
        return []
    
    def show_answer(self):
        """显示正确答案"""
        correct_answers = self.question_data.get('answer', [])
        if isinstance(correct_answers, int):
            correct_answers = [correct_answers]
        
        for i, (frame, label) in enumerate(zip(self.option_frames, self.option_labels)):
            if i in correct_answers:
                # 正确答案：绿色背景和边框
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #E8F5E9;
                        border: 2px solid #4CAF50;
                        border-radius: 10px;
                        padding: 0px;
                    }
                """)
                label.setStyleSheet("""
                    padding: 0px;
                    background-color: transparent;
                    border: none;
                """)
                # 更新标签文本，添加绿色标记
                original_text = label.text()
                if "✓" not in original_text:
                    label.setText(original_text.replace(f"{chr(65 + i)}.", f"✓ {chr(65 + i)}."))
            elif self.option_buttons[i].isChecked() and i not in correct_answers:
                # 错误答案：红色背景和边框
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #FFEBEE;
                        border: 2px solid #F44336;
                        border-radius: 10px;
                        padding: 0px;
                    }
                """)
                label.setStyleSheet("""
                    padding: 0px;
                    background-color: transparent;
                    border: none;
                """)
                # 更新标签文本，添加红色标记
                original_text = label.text()
                if "✗" not in original_text:
                    label.setText(original_text.replace(f"{chr(65 + i)}.", f"✗ {chr(65 + i)}."))


class QuizApp(QMainWindow):
    """答题软件主窗口"""
    
    def __init__(self):
        super().__init__()
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.total_questions = 0
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("简易答题软件")
        self.setGeometry(100, 100, 1100, 850)
        
        # 设置窗口背景色
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
        """)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部工具栏
        toolbar_frame = QFrame()
        toolbar_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(15)
        
        self.import_btn = QPushButton("📁 导入题目")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.import_btn.clicked.connect(self.import_questions)
        toolbar_layout.addWidget(self.import_btn)
        
        toolbar_layout.addStretch()
        
        # 进度信息
        info_frame = QFrame()
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        self.question_info_label = QLabel("题目: 0/0")
        self.question_info_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #424242;
        """)
        info_layout.addWidget(self.question_info_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
                height: 6px;
                background-color: #E0E0E0;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        info_layout.addWidget(self.progress_bar)
        
        info_frame.setLayout(info_layout)
        toolbar_layout.addWidget(info_frame)
        
        toolbar_frame.setLayout(toolbar_layout)
        main_layout.addWidget(toolbar_frame)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #E0E0E0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #BDBDBD;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9E9E9E;
            }
        """)
        
        self.question_widget = QWidget()
        self.question_layout = QVBoxLayout()
        self.question_layout.setContentsMargins(0, 0, 0, 0)
        self.question_widget.setLayout(self.question_layout)
        
        scroll_area.setWidget(self.question_widget)
        main_layout.addWidget(scroll_area, 10)  # 增加拉伸因子，让题目区域占据更多空间
        
        # 底部控制区域
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(12)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.prev_btn = QPushButton("◀ 上一题")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 12px 28px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #9E9E9E;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_question)
        self.prev_btn.setEnabled(False)
        button_layout.addWidget(self.prev_btn)
        
        button_layout.addStretch()
        
        self.submit_btn = QPushButton("✓ 提交答案")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_answer)
        button_layout.addWidget(self.submit_btn)
        
        button_layout.addStretch()
        
        self.next_btn = QPushButton("下一题 ▶")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 12px 28px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #FFE0B2;
                color: #9E9E9E;
            }
        """)
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        button_layout.addWidget(self.next_btn)
        
        bottom_layout.addLayout(button_layout)
        
        # 分数显示
        score_frame = QFrame()
        score_frame.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        score_layout = QHBoxLayout()
        score_layout.setContentsMargins(0, 0, 0, 0)
        
        self.score_label = QLabel("得分: 0/0")
        self.score_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1976D2;
        """)
        self.score_label.setAlignment(Qt.AlignCenter)
        score_layout.addWidget(self.score_label)
        score_frame.setLayout(score_layout)
        bottom_layout.addWidget(score_frame)
        
        bottom_frame.setLayout(bottom_layout)
        main_layout.addWidget(bottom_frame)
        
        central_widget.setLayout(main_layout)
        
        # 初始状态提示
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """显示欢迎信息"""
        welcome_label = QLabel("欢迎使用答题软件！\n\n请点击「导入题目」按钮导入题目文件（JSON格式）")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; color: #757575; padding: 50px;")
        self.question_layout.addWidget(welcome_label)
    
    def update_button_states(self):
        """更新按钮状态"""
        if not self.questions:
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < self.total_questions - 1)
    
    def parse_excel(self, file_path):
        """解析 Excel 文件并转换为题目列表"""
        try:
            workbook = load_workbook(file_path, data_only=True)
            sheet = workbook.active
            
            questions = []
            
            # 读取表头，确定列的位置
            # 从第一行开始查找，跳过说明行
            header_row = None
            for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_row=10, values_only=True), 1):
                row_values = [str(cell).strip() if cell else "" for cell in row]
                first_cell = row_values[0] if row_values else ""
                non_empty_count = sum(1 for val in row_values if val)
                
                # 跳过说明行：第一列包含"说明"且整行只有第一个单元格有内容（合并单元格的情况）
                if first_cell and "说明" in first_cell and non_empty_count <= 1:
                    continue
                
                # 查找表头行：必须同时包含"题目类型"列名和至少一个选项列或答案列
                # 表头行的特征：多个列都有内容，且包含明确的列名
                has_type_col = any(val == "题目类型" or (val.lower() == "type" and "question" not in val.lower())
                                  for val in row_values)
                has_options_col = any("选项" in val and val != "题目类型" or 
                                     "option" in val.lower() or 
                                     re.match(r'^[A-F]$', val.strip(), re.IGNORECASE) 
                                     for val in row_values)
                has_answer_col = any(val == "正确答案" or "答案" in val or 
                                    "answer" in val.lower() 
                                    for val in row_values)
                
                # 表头行应该有多个列，且包含题目类型列
                if has_type_col and non_empty_count >= 3 and (has_options_col or has_answer_col):
                    header_row = row_idx
                    break
            
            if header_row is None:
                # 如果没有找到明确的表头，尝试从第二行开始（第一行可能是说明）
                if sheet.max_row >= 2:
                    row2_values = [str(cell.value).strip() if cell.value else "" for cell in sheet[2]]
                    if any(val == "题目类型" or val.lower() == "type" for val in row2_values):
                        header_row = 2
                    else:
                        header_row = 1
                else:
                    header_row = 1
            
            # 读取表头，确定各列的位置
            headers = [str(cell.value).strip() if cell.value else "" for cell in sheet[header_row]]
            
            # 查找关键列的位置
            type_col = None
            question_col = None
            answer_col = None
            option_cols = []
            
            for idx, header in enumerate(headers):
                if not header:
                    continue
                    
                header_lower = header.lower().strip()
                header_original = header.strip()
                
                # 题目类型列
                if type_col is None:
                    if ("类型" in header_original and "题目" in header_original) or \
                       ("type" in header_lower and "question" not in header_lower) or \
                       header_lower == "type":
                        type_col = idx
                        continue
                
                # 题目列
                if question_col is None:
                    if ("题目" in header_original and "类型" not in header_original) or \
                       "question" in header_lower:
                        question_col = idx
                        continue
                
                # 答案列
                if answer_col is None:
                    if "答案" in header_original or "正确" in header_original or \
                       "answer" in header_lower:
                        answer_col = idx
                        continue
                
                # 选项列：选项A、选项B、选项1、选项2 或直接是 A、B、C、D
                if re.match(r'^选项[ABCDEF\d]+$', header_original, re.IGNORECASE) or \
                   re.match(r'^[ABCDEF]$', header_original, re.IGNORECASE) or \
                   ("选项" in header_original and header_original not in ["题目类型", "正确答案"]):
                    option_cols.append(idx)
            
            # 如果没找到选项列，尝试按位置推断（题目列之后，答案列之前）
            if not option_cols:
                start = max((question_col or 0) + 1, (type_col or 0) + 1)
                end = answer_col if answer_col else len(headers)
                if end > start:
                    option_cols = list(range(start, end))
            
            # 验证必要的列是否存在
            missing_cols = []
            if type_col is None:
                missing_cols.append("题目类型")
            if question_col is None:
                missing_cols.append("题目")
            if answer_col is None:
                missing_cols.append("正确答案")
            if not option_cols:
                missing_cols.append("选项列")
            
            if missing_cols:
                raise ValueError(f"Excel 文件格式不正确，缺少必要的列：{', '.join(missing_cols)}\n"
                               f"检测到的表头：{headers}\n"
                               f"请确保表头包含：题目类型、题目、选项A/B/C/D、正确答案")
            
            # 读取数据行
            for row_idx, row in enumerate(sheet.iter_rows(min_row=header_row + 1, values_only=True), header_row + 1):
                # 跳过空行
                if not any(cell for cell in row):
                    continue
                
                # 读取题目类型
                q_type = str(row[type_col]).strip() if row[type_col] else ""
                if not q_type:
                    continue  # 跳过没有类型的行
                
                # 标准化题目类型（支持中文和英文）
                q_type_lower = q_type.lower().strip()
                q_type_original = q_type.strip()
                
                # 支持中文：单选、多选题、单选题、多选
                if "单选" in q_type_original and "多选" not in q_type_original:
                    q_type = "single"
                elif "多选" in q_type_original:
                    q_type = "multiple"
                # 支持英文：single, multiple
                elif "single" in q_type_lower:
                    q_type = "single"
                elif "multiple" in q_type_lower:
                    q_type = "multiple"
                else:
                    raise ValueError(f"第 {row_idx} 行：题目类型 '{q_type}' 无效，应为：单选/多选 或 single/multiple")
                
                # 读取题目
                question = str(row[question_col]).strip() if row[question_col] else ""
                if not question:
                    raise ValueError(f"第 {row_idx} 行：题目内容为空")
                
                # 读取选项
                options = []
                for col_idx in option_cols:
                    if col_idx < len(row):
                        option = str(row[col_idx]).strip() if row[col_idx] else ""
                        if option:  # 只添加非空选项
                            options.append(option)
                
                if len(options) < 2:
                    raise ValueError(f"第 {row_idx} 行：选项数量不足（至少需要 2 个选项）")
                
                # 读取正确答案
                answer_str = str(row[answer_col]).strip() if row[answer_col] else ""
                if not answer_str:
                    raise ValueError(f"第 {row_idx} 行：正确答案为空")
                
                # 解析答案
                if q_type == "single":
                    # 单选题：可能是字母（A, B, C...）或数字（0, 1, 2...）
                    answer_str = answer_str.upper().strip()
                    if answer_str.isalpha():
                        # 字母转索引
                        answer = ord(answer_str) - ord('A')
                    elif answer_str.isdigit():
                        # 数字（可能是从1开始或从0开始）
                        answer = int(answer_str)
                        if answer > 0:
                            answer -= 1  # 转换为从0开始的索引
                    else:
                        raise ValueError(f"第 {row_idx} 行：单选题答案格式错误 '{answer_str}'")
                    
                    if answer < 0 or answer >= len(options):
                        raise ValueError(f"第 {row_idx} 行：答案索引 {answer} 超出选项范围")
                    
                else:  # multiple
                    # 多选题：用逗号分隔，可能是字母或数字
                    answer_parts = [p.strip().upper() for p in answer_str.split(',')]
                    answer = []
                    for part in answer_parts:
                        if part.isalpha():
                            idx = ord(part) - ord('A')
                        elif part.isdigit():
                            idx = int(part)
                            if idx > 0:
                                idx -= 1
                        else:
                            raise ValueError(f"第 {row_idx} 行：多选题答案格式错误 '{part}'")
                        
                        if idx < 0 or idx >= len(options):
                            raise ValueError(f"第 {row_idx} 行：答案索引 {idx} 超出选项范围")
                        answer.append(idx)
                    
                    answer = sorted(list(set(answer)))  # 去重并排序
                    if not answer:
                        raise ValueError(f"第 {row_idx} 行：多选题答案为空")
                
                # 添加到题目列表
                questions.append({
                    "type": q_type,
                    "question": question,
                    "options": options,
                    "answer": answer
                })
            
            if not questions:
                raise ValueError("Excel 文件中没有找到有效的题目")
            
            return questions
            
        except Exception as e:
            raise ValueError(f"解析 Excel 文件失败：{str(e)}")
    
    def import_questions(self):
        """导入题目"""
        file_path, file_type = QFileDialog.getOpenFileName(
            self,
            "选择题目文件",
            "",
            "Excel Files (*.xlsx *.xls);;JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                # 根据文件扩展名选择解析方式
                file_ext = Path(file_path).suffix.lower()
                
                if file_ext in ['.xlsx', '.xls']:
                    # Excel 文件
                    self.questions = self.parse_excel(file_path)
                else:
                    # JSON 文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 支持两种格式：直接是数组，或者包含questions字段的对象
                    if isinstance(data, list):
                        self.questions = data
                    elif isinstance(data, dict) and 'questions' in data:
                        self.questions = data['questions']
                    else:
                        raise ValueError("无效的题目文件格式")
                
                if not self.questions:
                    QMessageBox.warning(self, "警告", "题目文件为空！")
                    return
                
                # 验证题目格式
                for i, q in enumerate(self.questions):
                    if 'question' not in q or 'options' not in q or 'answer' not in q:
                        raise ValueError(f"第 {i+1} 题格式不正确，必须包含 question、options 和 answer 字段")
                    if not isinstance(q['options'], list) or len(q['options']) < 2:
                        raise ValueError(f"第 {i+1} 题选项数量不足")
                
                self.current_index = 0
                self.score = 0
                self.total_questions = len(self.questions)
                self.load_question()
                QMessageBox.information(self, "成功", f"成功导入 {self.total_questions} 道题目！")
                
            except json.JSONDecodeError:
                QMessageBox.critical(self, "错误", "JSON 文件格式错误！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入失败：{str(e)}")
    
    def load_question(self):
        """加载当前题目"""
        # 清空当前布局
        while self.question_layout.count():
            child = self.question_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.questions:
            # 如果没有题目，禁用所有按钮
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        
        # 创建题目组件
        question_widget = QuestionWidget(self.questions[self.current_index])
        self.question_layout.addWidget(question_widget)
        self.current_question_widget = question_widget
        
        # 更新信息
        self.question_info_label.setText(f"题目: {self.current_index + 1}/{self.total_questions}")
        
        # 更新进度条
        if self.total_questions > 0:
            progress = int((self.current_index + 1) / self.total_questions * 100)
            self.progress_bar.setValue(progress)
        
        # 更新按钮状态 - 确保在所有情况下都更新
        can_go_prev = self.current_index > 0
        can_go_next = self.current_index < self.total_questions - 1
        
        self.prev_btn.setEnabled(can_go_prev)
        self.next_btn.setEnabled(can_go_next)
        
        # 重置提交按钮
        self.submit_btn.setEnabled(True)
    
    def prev_question(self):
        """上一题"""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()
        # 确保按钮状态正确更新
        self.update_button_states()
    
    def next_question(self):
        """下一题"""
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            self.load_question()
        # 确保按钮状态正确更新
        self.update_button_states()
    
    def submit_answer(self):
        """提交答案"""
        if not hasattr(self, 'current_question_widget'):
            QMessageBox.warning(self, "提示", "请先导入题目！")
            return
        
        selected = self.current_question_widget.get_selected_answers()
        if not selected:
            QMessageBox.warning(self, "提示", "请先选择答案！")
            return
        
        correct_answers = self.questions[self.current_index].get('answer', [])
        if isinstance(correct_answers, int):
            correct_answers = [correct_answers]
        
        # 判断是否正确
        is_correct = sorted(selected) == sorted(correct_answers)
        
        if is_correct:
            self.score += 1
            QMessageBox.information(self, "结果", "回答正确！✓")
        else:
            correct_str = ", ".join([chr(65 + i) for i in correct_answers])
            QMessageBox.warning(self, "结果", f"回答错误！\n正确答案是: {correct_str}")
        
        # 显示正确答案
        self.current_question_widget.show_answer()
        
        # 更新分数
        self.score_label.setText(f"得分: {self.score}/{self.total_questions}")
        
        # 禁用提交按钮，防止重复提交
        self.submit_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 样式，跨平台一致
    
    window = QuizApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

