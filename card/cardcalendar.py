from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc


class CardCalendar(HTMLCalendar):

    def __init__(self, cards):
        super(CardCalendar, self).__init__()
        self.cards = self.group_by_day(cards)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            # print self.cards
            for k, v in self.cards.items():
                if day == k.day:
                    cssclass += ' filled'
                    body = ['<div>']
                    for card in v:
                        body.append('<a href="editcard/%d">' % card.id)
                        body.append(esc(card))
                        body.append(' - ' + esc(card.owner))
                        body.append('</a>')
                        body.append('</div>')
                    return self.day_cell(
                        cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(CardCalendar, self).formatmonth(year, month)

    def group_by_day(self, cards):
        field = lambda card: card.due_date
        return dict(
            [(due_date, list(items)) for due_date, items in groupby(
                cards, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
