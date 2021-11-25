SELECT * FROM table_name q WHERE NOT EXISTS(SELECT 1 FROM table_name WHERE промо_проверяемый = q.ранее_введённый_промокод AND проверяемый_id = q.записанный_в_базе_id)




promocode = input() # сюда  бота вводит промокод для пользователя
promo_in = input('Please, enter here your promocode: /n') # сюда пользователь вводит промокод

if promo_in == promocode:
    del promocode # удаляет переменную с промокодом, а значит, даже если польз
