# Kilometreden Mil çevirici
kilometers = float(input("Sayınızı Girin(Kilometre): "))

# conversion factor
conv_fac = 0.621371

# calculate miles
miles = kilometers * conv_fac
print('%0.2f Kilometre  %0.2f Mile Eşittir' 
%(kilometers,miles))
