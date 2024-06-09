# this is how many oreos a user eats; VVV ADD ONE MORE 9 IN THE END AND YOU EAT TOO MANY OREO!
daily_oreo_consumption = 9.374999999999999

# amount of calories per serving
one_serving_in_calories = 160

# 1 serving of sodium amount in mg
one_serving_in_sodium = 190

# 1 serving of carbohydrate amount in g
one_serving_in_carbohydrate = 25

# 1 serving of fat in g
one_serving_in_fat = 7

# serving size of oreos
one_serving = (one_serving_in_calories + one_serving_in_carbohydrate + one_serving_in_fat + one_serving_in_sodium)

# amount of calories per oreo
one_oreo_in_calories = one_serving_in_calories/3

# amount of sodium per oreo on mg
one_oreo_in_sodium = one_serving_in_sodium/3

# amount of carbohydrate per oreo in g
one_oreo_in_carbohydrates = one_serving_in_carbohydrate/3

# amount of fat per oreo in g
one_oreo_in_fat = one_serving_in_fat/3

# what's inside 1 oreo
one_oreo = (one_oreo_in_calories, "calories", one_oreo_in_sodium,  "mg", one_oreo_in_carbohydrates,  "g", one_oreo_in_fat,  "g")

print(one_oreo)

# consumption of daily oreo cal
daily_oreo_consumption_calories = (one_oreo_in_calories * daily_oreo_consumption, "calories")

# consumption of daily oreo sodium
daily_oreo_consumption_sodium = (one_oreo_in_sodium * daily_oreo_consumption, "mg")

# consumption of daily oreo carbs
daily_oreo_consumption_carbohydrate = (one_oreo_in_carbohydrates * daily_oreo_consumption, "g")

# consumption of daily oreo fat
daily_oreo_consumption_fat = (one_oreo_in_fat * daily_oreo_consumption, "g")


# consumption of all the macros
all_daily_consumption_oreos = (daily_oreo_consumption_calories, daily_oreo_consumption_sodium, daily_oreo_consumption_carbohydrate, daily_oreo_consumption_fat)

# I ran into this error so i'll make another variable -- "TypeError: '>' not supported between instances of 'tuple' and 'int'"
one_daily_oreo_consumption_calories = (one_oreo_in_calories * daily_oreo_consumption)


print(daily_oreo_consumption_calories)

print(all_daily_consumption_oreos)


if (one_daily_oreo_consumption_calories >= 500):
    print("Stop eating these darn delicious cookies!")
    

    
else:
    print("Have another Oreo!")
     
     
     
     
     
     
     