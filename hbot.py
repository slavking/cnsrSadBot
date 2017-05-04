import datetime
from time import strftime,gmtime
#import timeParser

#botanswers

country = 'default'



def get_time3():
	today = datetime.date.today()
	return (str(today.strftime('Today is %d %b %Y.')))

def get_time2():
	return (strftime('Time in GMT: %H:%M:%S', gmtime()))

def get_shawty(nig):
        return (str('fuck youse niggers' + nig ))

answers = {
'.hbot':'Welcome to hohilbot, this message is really helpful.',
'.habout':'This bot is completely random because it might work but also might not.',
'.hdate':get_time3(),
'.htimeK':get_time2(),
'.nigger':get_shawty(nigger)
}
