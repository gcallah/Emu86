from selenium import webdriver

from unittest import TestCase, main

link = {
    '1': 'area.asm',
    '2': 'arithmetic_expression.asm',
    '3': 'arithmetic_shift.asm',
    '4': 'array.asm',
    '5': 'array_average_test.asm',
    '6': 'cel_to_fah.asm',
    '7': 'change_array_elem_test.asm',
    '8': 'data.asm',
    '9': 'int_square_root.asm',
    '10': 'key_test.asm',
    '11': 'log.asm',
    '12': 'loop.asm',
    '13': 'mem_register_test.asm',
    '14': 'power.asm',
    '15': 'sum_test.asm'
}

mips_link = {
    '1': 'area.asm',
    '2': 'arithmetic_expression.asm',
    '3': 'arithmetic_shift.asm',
    '4': 'array.asm',
    '5': 'array_average_test.asm',
    '6': 'cel_to_fah.asm',
    '7': 'change_array_elem_test.asm',
    '8': 'data.asm',
    '9': 'int_square_root.asm',
    '10': 'log.asm',
    '11': 'loop.asm',
    '12': 'power.asm',
    '13': 'sum_test.asm'
}


class TestLink(TestCase):

    def load_page(self):
        self.driver.get('http://www.emu86.org/')

    def close_page(self):
        self.driver.quit()

    def get_by_x_path(self, value):
        return self.driver.find_element_by_xpath(value)

    def getById(self, id):
        return self.driver.find_element_by_id(id)

    def link_test(self, flag):
        self.driver = webdriver.Chrome()
        num_links = 16
        if flag > 2:
            num_links = 14
        for sample in range(1, num_links):
            self.load_page()
            main_x_path = '//*[@id="content-main"]/div/details[2]/'
            self.get_by_x_path('//*[@id="user-tools"]/a[2]').click()
            self.get_by_x_path(main_x_path + 'summary').click()
            lang_select = main_x_path + 'details[' + str(flag) + ']/summary'
            self.get_by_x_path(lang_select).click()
            sub_path = 'details[' + str(flag) + ']/ul/li['
            sub_path += str(sample) + ']/a'
            self.get_by_x_path(main_x_path + sub_path).click()
            link_clicked = 'https://github.com/gcallah/Emu86/blob/master/tests/'
            if flag == 1:
                link_clicked += 'Intel/' + link[str(sample)]
            elif flag == 2:
                link_clicked += 'ATT/' + link[str(sample)]
            else:
                if flag == 3:
                    link_clicked += 'MIPS_ASM/'
                elif flag == 4:
                    link_clicked += 'MIPS_MML/'
                else:
                    link_clicked += 'RISCV/'
                link_clicked += mips_link[str(sample)]
            self.assertEqual(self.driver.current_url, link_clicked)
        self.close_page()

    def test_links(self):
        for flag in range(1, 6):
            self.link_test(flag)


if __name__ == '__main__':
    main()
