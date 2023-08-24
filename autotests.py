from time import sleep
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_data import AuthForm, CodeForm


# AUT-01
def test_check_visual_match(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('pic_01.jpg')


# AUT-02
def test_check_default_phone(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# AUT-03
def test_check_automatic_change_tub(selenium):
    form = AuthForm(selenium)

    # вводим Мобильный телефон
    form.username.send_keys('+79139139113')
    form.password.send_keys('Test1234567890')
    sleep(5)

    assert form.placeholder.text == 'Мобильный телефон'

    # очистить поле ввода логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим Электронную почту
    form.username.send_keys('test@mail.ru')
    form.password.send_keys('Test1234567890')
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'

    # очистить поле ввода логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим Логин
    form.username.send_keys('User1234')
    form.password.send_keys('Test1234567890')
    sleep(5)

    assert form.placeholder.text == 'Логин'

    # очистить поле ввода логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим Лицевой счёт
    form.username.send_keys('012345678910')
    form.password.send_keys('Test1234567890')
    sleep(5)

    assert form.placeholder.text == 'Лицевой счёт'


# AUT-05
def test_check_user_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # нажимаем на фразу "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    title_page = form.driver.execute_script("return window.document.title")

    assert title_page == 'User agreement'


# AUT-06
def test_check_success_auth_phone(selenium):
    form = AuthForm(selenium)

    # вводим телефон и пароль
    form.username.send_keys('+79139139113')
    form.password.send_keys('Test1234567890')
    sleep(5)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# AUT-07
def test_check_failure_auth_phone(selenium):
    form = AuthForm(selenium)

    # вводим телефон и пароль
    form.username.send_keys('+79139139113')
    form.password.send_keys('Test1234')
    sleep(5)
    form.btn_click()

    message_err = form.driver.find_element(By.ID, 'form-error-message')
    assert message_err.text == 'Неверный логин или пароль'


# AUT-08
def test_check_success_auth_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys('test@mail.ru')
    form.password.send_keys('Test1234567890')
    sleep(5)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# AUT-09
def test_check_failure_auth_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys('tost@mail.ru')
    form.password.send_keys('Test1234567890')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# AUT-14
def test_check_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'oauth.vk.com'


# AUT-15
def test_check_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'


# AUT-16
def test_check_auth_mail_ru(selenium):
    form = AuthForm(selenium)
    form.mail_ru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


# AUT-17
@pytest.mark.xfail(reason='Кнопка авторизации через Паспорт Яндекс не срабатывает с первого раза')
def test_check_auth_yandex(selenium):
    form = AuthForm(selenium)
    form.yandex_btn.click()
    sleep(3)

    assert form.get_base_url() == 'passport.yandex.ru'


# AUT-21
def test_access_recovery(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# AUT-22
def test_check_registration_form(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'