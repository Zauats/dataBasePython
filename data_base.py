import os
import random
import msvcrt
import time
import sys
import re


os.system("mode con cols=150 lines=30")
clear = lambda: os.system('cls')

def lsort(lists, index): 
	"""Сортирует список по определенному индексу""" 
	if len(lists) <= 1:
		return lists
	else:
		q = random.choice(lists)
		s_nums = []
		m_nums = []
		e_nums = []
		for n in lists:
			try:
				if int(n[index]) < int(q[index]):
					s_nums.append(n)
				elif int(n[index]) > int(q[index]):
					m_nums.append(n)
				else:
					e_nums.append(n)
			except:
				if n[index] < q[index]:
					s_nums.append(n)
				elif n[index] > q[index]:
					m_nums.append(n)
				else:
					e_nums.append(n)
		return lsort(s_nums, index) + e_nums + lsort(m_nums, index)


def round(num, big=False):
	num = num / 1

	number = str(num).split('.')
	num = int(number[0])
	
	if big and number[1] != '0' and (number[0][0] != '-'):
			num += 1

	return num



class Table():
	"""Table - это класс, который представляет одну таблицу и все ее методы без графической оболочки.
		Возможно запрещенные методы: list.append(), 'str'.join(list), list.pop(), list.replace(), list.index(), list.extend(),
									 random.choise(), os.system(), isinstance(), raise, abs(), msvcrt.getch(), keyboard.read_key(), max(), split()

		Список методов:
		input_element - метод, позволяющий добавить или изменить информацию в таблице.
					 На вход принимает координаты изменяемой ячейки(x, y) и саму информацию.
					 Если координаты находятся вне таблицы, бросает исключение ValueError.
					 Если координаты переданы неправильного типа, бросает исключение TypeError
					 Функция ничего не озвращает

		delete_element - метод, позволяющий удалить информацию из таблицы. Принимает координаты изменяемой переменной.
						 Бросает те же ошибки, что и input_element. Ничего не возвращает

		search_element - метод, позволяющий найти совпадения переданного значения в таблице. 
						 Функция принимает элемент для поиска и список колонн в которых следует производить поиск. 
						 По умолчанию, функция ищет совпадения по всей таблице. Вернет исключение, если переданный столбец отсутствует в таблице
		sort_elemtnts - метод, позволяющий сортировать информацию по столбцам. Принимает индекс столбца, возвращает исключение, если такого нет. 
						"""




	def __init__(self, right,  *args, table=None, regex=None, **kwargs, ):
		#разрешения на [ввод данных, передвежение курсора, прокрутывание таблицы, поиск и сортировку]
		if 'name' in kwargs:
			self.name = kwargs['name']

		if table != None:
			self.table = table
		else:
			self.width = len(args)
			self.table = [list(args), ['' for i in (self.width) * ' ']]  # создается cтруктура таблицы
			self.table[0].append("0")
			self.table[1].append("1")
		if regex is None:
			# self.regex = ['[qwertyuiopasdfghjklzxcvbnm.,""1234567890-+=йцукенгшщзхъфывапролджэячсмитьбю/ №%()]*' for i in (self.width) * " "]
			self.regex = [r'[\w\d\s№%()/+="".,-]*' for i in self.width * " "]

		else:
			self.regex = regex

		self.search_column = 0
		self.search_string = ''
		self.id_list = ['0', '1']
		self.cursor = [0, 0]
		self.id1 = 0
		self.id2 = 10
		self.right = right

	def move_cursor(self, simbol):
		x = 0
		y = 0
		try:
			if (re.fullmatch(self.regex[self.cursor[0]] + r"|\s*", self.table[int(self.id_list[self.cursor[1]])][self.cursor[0]], flags=re.IGNORECASE) is not None) or int(self.id_list[self.cursor[1]]) == 0:
				if simbol == "←": x = -1
				elif simbol == "↑":	y = -1
				elif simbol == "→": x = 1
				elif simbol == "↓":	y = 1
		except:
			pass

		self.search_element()
		if self.cursor[0] + x < 0: self.cursor[0] = self.width - 1
		elif self.cursor[0] + x > self.width - 1: self.cursor[0] = 0
		elif self.cursor[1] + y < 0: self.cursor[1] = len(self.id_list) - 1
		elif self.cursor[1] + y > len(self.id_list) - 1: self.cursor[1] = 0
		else:
			self.cursor[0] += x
			self.cursor[1] += y

	def input_element(self, x, y, new_data): 
		"""
		   4. Проверка на то, что в конец таблицы добавился пустой список при добавлении элемента в конец
		   """
		new_data = str(new_data)
		if not isinstance(x, int) or not isinstance(y, int) or not isinstance(new_data, str):
			raise TypeError('x и y должны быть числом, new_data должна быть строкой')

		elif (abs(x + 1) > self.width) or (abs(y + 1) > len(self.table)): 
			raise ValueError('Такого элемента в таблице нет')

		elif y + 1 == len(self.table) and new_data.replace(' ','').replace('\n', '').replace('\t', '').replace('\v', '') != '':
			new_string = ['' for i in self.width * ' ']
			new_string.append(str(len(self.table)))
			self.table.append(new_string)
			self.table[y][x] = new_data		
		else:
			self.table[y][x] = new_data
		
	def delete_element(self, x, y):
		"""1. Проверка на то, что бросается ValueError при неккоректных координатах
		   2. Бросается исключение TypeError при передачи неккоректных данных
		   3. удаляется список, если он остается пустым
		   4. последний список не удаляется и остается пустым нисмотря ни на что
		"""
		self.input_element(x, y, '')

		if (''.join(self.table[y][:-1]) == '') and (y + 1 < len(self.table)):
			self.table.pop(y)
		for i in range(len(self.table)):
			self.table[i][-1] = str(i)

	def search_element(self):
		id_list = ['0']
		for i in range(len(self.table) - 1):
			if self.search_string in self.table[i + 1][self.search_column]:
				id_list.append(self.table[i + 1][-1])
		if str(len(self.table) - 1) not in id_list:
			id_list.append(str(len(self.table) - 1))
		self.id_list = id_list[self.id1:self.id2]

	def sort_elements(self):
		new_table = [self.table[0]]
		new_table.extend(lsort(self.table[1:-1], self.cursor[0]))
		new_table.append(self.table[-1])
		self.table = new_table
		for i in range(len(self.table)):
			self.table[i][-1] = str(i)

	def print_table(self, max_string=25):
		max_x_list = []
		max_y_list = []
		string = ''
		table = self.table
		for i in range(self.width + 1):
			len_x = len(max(table, key=lambda x : len(x[i]))[i])

			if len_x > max_string:
				len_x = max_string
			max_x_list.append(len_x)

		for y in table:
			max_value = len(max(y, key=lambda y : len(y)))
			max_value = round(max_value / max_string, True)
			if max_value == 0:
				max_value = 1
			max_y_list.append(max_value)

		if self.right[3]:
			string += 'Поиск: ' + self.search_string + '\n'
		first_i = 0
		choise = False
		self.search_element()

		id1 = 1;
		id2 = len(self.id_list)
		if self.cursor[1] > 5:
			id1 = self.cursor[1] - 5
		if 5 < len(self.id_list):
			id2 = self.cursor[1] + 5
			if self.cursor[1] <= 5:
				id2 += 5 - self.cursor[1]


		id_list = self.id_list
		for y, max_y,  in zip(table, max_y_list):
			if y[-1] in id_list:
				for i, max_x in enumerate(max_x_list):
					open_color = ''
					close_color = ''
					if (i == self.cursor[0] and first_i == self.cursor[1]) or (i == self.cursor[0] and first_i == self.cursor[1] + 1):
						open_color = '\x1b[31m'
						close_color = '\x1b[0m'
					if first_i == 0:
						if i == 0: simbol = '╔'
						else: simbol = '╦'
					else:			
						if i == 0: simbol = '╠'
						else: simbol = '╬'
					string += simbol + open_color + '═' * (max_x + 2) + close_color


				if first_i == 0: string += '╗\n'
				else: string += '╣\n'

				y = list(y)
				for i in range(max_y):
					start , end = 0, max_string
					for x, max_x in enumerate(max_x_list):

						max_x -= len(y[x])
						if (x == self.cursor[0] and first_i == self.cursor[1]): 
							string += '\x1b[31m║ ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' \x1b[0m'
						elif  (x == self.cursor[0] + 1 and first_i == self.cursor[1]):
							string += '\x1b[31m║\x1b[0m ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' '
						else:
							string += '║ ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' '

						y[x] = y[x][start + max_string:]
					start += max_string
					end += max_string

					if (self.width - 1 == self.cursor[0] and first_i == self.cursor[1]):
						string += '\x1b[31m║\x1b[0m\n'
					else:
						string += '║\n'
				first_i +=1

		for i, max_x in enumerate(max_x_list):
			simbol = '╩'
			if i == 0:
				simbol = '╚'
			if i == self.cursor[0] and len(self.table) - 1 == self.cursor[1]:
				string += simbol + '\x1b[31m═\x1b[0m' * (max_x + 2)
			else:
				string += simbol + '═' * (max_x + 2)

		string += '╝'

		# if first_i
		return string

	def event_handler(self, event):
		if self.right[0] or (self.cursor[1] == 0 and self.right[3]):
			if event == "del":
				if self.cursor[1] == 0:
					self.search_string = ''
				else:
					num = 0
					for string in (len(self.table[0]) - 1) * " ":
						self.delete_element(num, int(self.id_list[self.cursor[1]]))
						num += 1

			elif event  == "Backspace":
				if self.cursor[1] == 0:
					self.search_column = self.cursor[0]
					self.search_string = self.search_string[:-1]
				else:
					field = self.table[int(self.id_list[self.cursor[1]])][self.cursor[0]]
					field = field[:len(field) - 1]
					self.input_element(self.cursor[0], int(self.id_list[self.cursor[1]]), field)
			elif event.lower() in "qwertyuiopasdfghjklzxcvbnm.,""1234567890-+=йцукенгшщзхъфывапролджэячсмитьбю/ №%()": # символ, который можно ввести
				if self.cursor[1] == 0:
					self.search_column = self.cursor[0]
					self.search_string += event
				else:
					field = self.table[int(self.id_list[self.cursor[1]])][self.cursor[0]]
					field += event
					self.input_element(self.cursor[0], int(self.id_list[self.cursor[1]]), field)

		if self.right[1]:
			if event == "←" or event == "↑" or event == "↓" or event == "→":
				self.move_cursor(event)
		
		if self.right[2]:
			if event == "ctrl+↑" and self.id1 > 0:
				self.id1 -= 1
				self.id2 -= 1
			elif event == "ctrl+↓" and (self.id2 < len(self.table) + 1):
				self.id1 += 1	
				self.id2 += 1

		if self.right[3] and event == "Enter" and int(self.id_list[self.cursor[1]]) == 0:
			self.sort_elements()
			clear()
			print(self.print_table())
					 




class Interface():
	def __init__(self, **kwargs):
		
		self.menu = Table([False, True, False, False], "Создать новую таблицу")
		self.menu.input_element(0, 1, "Загрузить существующую")
		self.menu.table = self.menu.table[:-1]

		self.saved_tables = Table([False, True, True, True], "Пустая таблица")
		with open('C:\\Users\\пользователь\\DataBase\\csacnn3ejch834hcscjnj2lwdc9cdioj.txt', encoding='UTF-8') as f:
			files = f.read()
			files = files.split('\n')
			for i, file in enumerate(files):
				self.saved_tables.input_element(0, i + 1, file)

		self.help_table = Table([False, False, True, False], 'клавиша или сочетание', 'действие')
		self.help_table.input_element(0, 1, 'f1')
		self.help_table.input_element(0, 2, 'ctrl + s')
		self.help_table.input_element(0, 3, 'ctrl + fномер')
		self.help_table.input_element(0, 4, 'esc')
		self.help_table.input_element(0, 5, 'del')
		self.help_table.input_element(0, 6, 'Enter')
		self.help_table.input_element(0, 7, 'Стрелочки')
		self.help_table.input_element(0, 8, 'ctrl+Стрелочки')

		self.help_table.input_element(1, 1, 'помощь')
		self.help_table.input_element(1, 2, 'сохранить таблицу')
		self.help_table.input_element(1, 3, 'переход между таблицами')
		self.help_table.input_element(1, 4, 'назад или выход')
		self.help_table.input_element(1, 5, 'удалить информацию в ячейке')
		self.help_table.input_element(1, 6, 'Сортировка/выбор элемента')
		self.help_table.input_element(1, 7, 'Перемещение курсора')
		self.help_table.input_element(1, 8, 'прокрутка таблицы')


		self.tables = kwargs
		self.tables['help'] = self.help_table
		self.tables['menu'] = self.menu
		self.tables['saved_tables'] = self.saved_tables
		self.tables_list = list(self.tables.keys())
		self.cursor = 4
		self.check = True



	def run(self):
		while self.check:
			self.main()
			clear()
			print(self.tables[self.tables_list[self.cursor]].print_table())
		clear()
		print("В этом наше полномочие, все")



	def event_handler(self):
		key = msvcrt.getwch()
				
		if key == u'\u0000':
			key = msvcrt.getwch()
			if ord(key) == 59:
				return "f1"
			elif ord(key) == 83:
				return "del"
			elif ord(key) == 94:
				return "ctrl+f1"
			elif ord(key) == 95:
				return "ctrl+f2"
			elif ord(key) == 96:
				return "ctrl+f3"
			else:
				return "Ошибка"

		elif key == u'\u00E0':
			key = msvcrt.getwch() 
			if ord(key) == 75:
				return "←"
			elif ord(key) == 72:
				return "↑"
			elif ord(key) == 77:
				return "→"
			elif ord(key) == 80:
				return "↓"
			elif ord(key) == 141:
				return "ctrl+↑"
			elif ord(key) == 145:
				return "ctrl+↓"
			else:
				return "Ошибка"

		elif key == chr(13):
			return "Enter"
		elif key == chr(19):
			return "ctrl+s"

		elif key == chr(27):
			return "esc"
		elif key == chr(8):
				return "Backspace"
		else:
			return key


	def main(self):
		choise_table = self.tables[self.tables_list[self.cursor]]
		key = self.event_handler()
		if self.cursor == 4:
				key_menu = ''
				while key_menu != "Enter": 
					clear()
					print("выберете пункт:")
					choise_table.event_handler(key_menu)
					print(choise_table.print_table())
					if (key_menu == 'esc'): 
						clear()
						print("Вот и все")
						sys.exit()
					key_menu = self.event_handler()
				if choise_table.cursor[1] == 0:
					table_num = 0
					with open(f'C:\\Users\\пользователь\\DataBase\\defaultFile.txt', encoding="UTF-8") as f:
							table = list()
							for string in f:
								string = string.split(',')[:-1]
								table.append(string)
								if (len(string) == 0):
									table = table[:-1]
									self.tables[self.tables_list[table_num]].table = table
									table = list()
									table_num += 1
					self.cursor = 0

				elif choise_table.cursor[1] == 1:
					key_menu = ''
					self.cursor = 5
					choise_table = self.tables[self.tables_list[self.cursor]]
					while key_menu != "Enter": 
						clear()
						print("выберете пункт:")
						choise_table.event_handler(key_menu)
						print(choise_table.print_table())
						key_menu = self.event_handler()
						if (key_menu == 'esc'): 
							self.cursor = 4
							key_menu = "Enter"

					if self.cursor != 4:
						file = self.tables['saved_tables'].table[int(self.tables['saved_tables'].id_list[self.tables['saved_tables'].cursor[1]])][self.tables["saved_tables"].cursor[0]]
						if file == "Пустая таблица":
							file = "defaultFile"
						table_num = 0
						with open(f'C:\\Users\\пользователь\\DataBase\\{file}.txt', encoding="UTF-8") as f:
							table = list()
							for string in f:
								string = string.split(',')[:-1]
								table.append(string)
								if (len(string) == 0):
									table = table[:-1]
									self.tables[self.tables_list[table_num]].table = table
									table = list()
									table_num += 1
						self.cursor = 0

		elif key == "f1":
			self.cursor = 3

		elif key == "esc":
			if self.cursor == 3:
				self.cursor = 0
			else:
				clear()
				print("Вы выхода нажмите Esc еще раз. Все несохраненные изменения не сохранятся")
				event = self.event_handler()
				if event == "esc":
					self.cursor = 4

		elif key == "Enter":
			if int(choise_table.id_list[choise_table.cursor[1]]) == 0:
				choise_table.sort_elements()
			elif choise_table.cursor[0] == 0 and self.cursor == 0:
				table = self.tables[self.tables_list[1]]
				choise_key = ""
				while choise_key != "Enter":
					clear()
					print('выберете какой-нибудь пункт: ')
					table.event_handler(choise_key)
					print(table.print_table())
					choise_key = self.event_handler()
				ful_name = table.table[int(table.id_list[table.cursor[1]])][0]
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), ful_name)

			elif choise_table.cursor[0] == 1 and self.cursor == 0:
				table = self.tables[self.tables_list[2]]
				choise_key = ''
				while choise_key != "Enter":
					clear()
					print('выберете какой-нибудь пункт: ')
					table.event_handler(choise_key)
					print(table.print_table())
					choise_key = self.event_handler()
				ful_name = table.table[int(table.id_list[table.cursor[1]])][0]
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), ful_name)
							
		elif key == "ctrl+f1":
			self.cursor = 0
		elif key == "ctrl+f2":
			self.cursor = 1
		elif key == "ctrl+f3":
			self.cursor = 2
		elif key == "ctrl+s":
			clear()
			save = input("Введите название вашего сохранения: ")
			with open('C:\\Users\\пользователь\\DataBase\\csacnn3ejch834hcscjnj2lwdc9cdioj.txt', 'a', encoding='UTF-8') as f:		
				f.write(save + '\n')

			with open(f'C:\\Users\\пользователь\\DataBase\\{save}.txt', 'w', encoding='UTF-8') as f:
				for i in range(3):
					table = self.tables[self.tables_list[i]].table
					for string in table:
						for field in string:
							f.write(field + ',')
						f.write('\n')
					f.write('\n')
			print('\a')

		choise_table.event_handler(key)

if __name__ == "__main__":
	work_table = Table([True, True, True, True], 'Практическая работа', 'Студент', 'Вариант', 'Уровень задания', 'Дата сдачи', 'Оценка', name='таблица выполнения работ',
					   regex=[r'[\w№ -]+', r'[ ]*[\w]+[ ][\w]+[ ][\w]+[ ]*', r'[ ]*[\d]{1,2}[ ]*', r'[ ]*[\d]{1,2}[ ]*', r'[ ]*[\d]{4}[.][0-9]{2}[.][0-9]{2}[ ]*', r'[ ]*[\d]{1}[ ]*'])
	practic_table = Table([True, True, True, True], 'Название работы', 'Количество часов', name='таблица практических работ', regex=[r'[\w№ -]+', r'[ ]*[0-9]{1,2}[ ]*'])
	student_table = Table([True, True, True, True], 'ФИО', 'Оцека', name='таблица студентов', regex=[r'[ ]*[\w]+[ ][\w]+[ ][\w]+[ ]*', r'[ ]*[0-5]{1}[ ]*'])
	
	interface = Interface(main=work_table, table0=practic_table, table1=student_table)
	interface.run()
