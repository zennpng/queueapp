#!/usr/bin/env python
# coding: utf-8

# In[3]:

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from libdw import pyrebase

url = 'DBURL'
apikey = 'APIKEY'  
config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout= BoxLayout(orientation='vertical',spacing=4)

        canteen_population= Label(text = "[u]Canteen[/u]",markup=True,font_size=65,size_hint=(1,0.15))
        self.layout.add_widget(canteen_population)

            
        people_from_firebase=db.child('people_in_canteen').get()
        self.number=Label(text=str(people_from_firebase.val()),font_size=90, size_hint=(1,0.1))
        self.layout.add_widget(self.number)
        
        
        def poplevel():
            return round(100*(people_from_firebase.val())/(820),2)
            
        self.population=Label(text='people currently in the canteen (' +str(poplevel()) +'% full)',font_size=48, size_hint=(1,0.2))
        self.layout.add_widget(self.population)
        
        reset_button_home=Button(text='Refresh',background_normal='',background_color=(0.2,0.5,0.1,0.5),size=(30,30),size_hint=(0.4,0.05))
        reset_button_home.bind(on_press=self.callback)
        self.layout.add_widget(reset_button_home)
        
        Chicken_rice = Button(text='More details on Chicken Rice stall',background_normal='',background_color=(0,0.2,0.3,0.5),size_hint=(1,0.2))
        Chicken_rice.bind(on_press=self.change_to_Chickenrice)
        self.layout.add_widget(Chicken_rice)
        
        
        Mixed_vegrice = Button(text='More details on Mixed Vegetable Rice Stall',background_normal='',background_color=(0,0.2,0.3,0.5), size_hint=(1,0.2))
        Mixed_vegrice.bind(on_press=self.change_to_Mixedrice)
        self.layout.add_widget(Mixed_vegrice)
        
        QuitApp = Button(text='Exit App', size_hint=(1,0.1))
        QuitApp.bind(on_press=self.quit_app)
        self.layout.add_widget(QuitApp)
        
        self.add_widget(self.layout)
        pass
    
    
    def callback(self,instance):
        people_from_firebase=db.child('people_in_canteen').get()
        self.number.text=str(people_from_firebase.val())

    def change_to_Chickenrice(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Chicken_rice_stall'
        
    def change_to_Mixedrice(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Mixed_rice_stall'   
        

    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()
    
    
class Chickenrice(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout= GridLayout(cols = 1)
        
        title_text=Label(text='[u]Chicken Rice Stall[/u]',markup=True, font_size=74)
        self.layout.add_widget(title_text)
        
        self.sensor1=db.child('stall1').get()
        self.sensor1_state=str(self.sensor1.val())
        
        def crowded(ss):
            if ss == 'blocked':
                return 'High'
            else:
                return 'Low to Normal'
        self.crowd=Label(text=('Crowd: '+crowded(self.sensor1_state)),font_size=58)
        self.layout.add_widget(self.crowd)
        
        def qtime(ss):
            if ss == 'blocked':
                return 'more than 5 minutes'
            else:
                return 'less than 5 minutes'

        
        self.Q_time=Label(text='Approximated wait time: '+ qtime(self.sensor1_state))
        self.layout.add_widget(self.Q_time)
        
        reset_button_chicken=Button(text='Refresh',background_normal='',background_color=(0.2,0.5,0.1,0.5),size_hint=(0.2,0.2))
        reset_button_chicken.bind(on_press=self.callback2)
        self.layout.add_widget(reset_button_chicken)
        
        
        Backtomenu = Button(text='Back to Home')
        Backtomenu.bind(on_press=self.change_to_menu)
        self.layout.add_widget(Backtomenu)
        
        self.add_widget(self.layout)
        
        
    def callback2(self,instance):
        def crowded(ss):
            if ss == 'blocked':
                return 'High'
            else:
                return 'Low to Normal'
        
        def qtime(ss):
            if ss == 'blocked':
                return 'more than 5 minutes'
            else:
                return 'less than 5 minutes'
            
        sensor1=db.child('stall1').get()
        sensor1_state=sensor1.val()
        self.crowd.text='Crowd: ' + crowded(sensor1_state)
        self.Q_time.text='Approximated wait time: '+ qtime(sensor1_state)
        
    def change_to_menu(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

        

class Mixedrice(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout= GridLayout(cols = 1)
        
        title_text=Label(text='[u]Mixed Vegetable Rice Stall[/u]',markup=True, font_size=74)
        self.layout.add_widget(title_text)
        
        self.sensor2=db.child('stall2').get()
        self.sensor2_state=str(self.sensor2.val())
        
        def crowded2(ss):
            if ss == 'blocked':
                return 'High'
            else:
                return 'Low to Normal'
            
        self.crowd2=Label(text='Crowd: '+crowded2(self.sensor2_state),font_size=58)
        self.layout.add_widget(self.crowd2)
        
        def qtime2(ss):
            if ss == 'blocked':
                return 'more than 7 minutes'
            else:
                return 'less than 7 minutes'
        
        self.Q2_time=Label(text='Approximated wait time: '+ qtime2(self.sensor2_state))
        self.layout.add_widget(self.Q2_time)
        
        reset_button_mixed=Button(text='Refresh',background_normal='',background_color=(0.2,0.5,0.1,0.5),size=(30,30),size_hint=(0.2,0.2))
        reset_button_mixed.bind(on_press=self.callback3)
        self.layout.add_widget(reset_button_mixed)
        
        
        Backtomenu = Button(text='Back to Home')
        Backtomenu.bind(on_press=self.change_to_menu)
        self.layout.add_widget(Backtomenu)
        
        self.add_widget(self.layout)
        
    def callback3(self,instance):
        def crowded2(ss):
            if ss == 'blocked':
                return 'High'
            else:
                return 'Low to Normal'
        def qtime2(ss):
            if ss == 'blocked':
                return 'more than 7 minutes'
            else:
                return 'less than 7 minutes'
            
        sensor2=db.child('stall2').get()
        sensor2_state=sensor2.val()
        self.crowd2.text='Crowd: '+crowded2(sensor2_state)
        self.Q2_time.text='Approximated wait time: '+qtime2(sensor2_state)
        
    def change_to_menu(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

        
class SwitchScreenApp(App):
    def build(self):
        Window.clearcolor = (0,0.5,0.5,0.5)
        sm = ScreenManager()
        ms = MainScreen(name='menu')
        st = Chickenrice(name='Chicken_rice_stall')
        st2 = Mixedrice(name='Mixed_rice_stall')

        sm.add_widget(ms)
        sm.add_widget(st)
        
        sm.add_widget(st2)
        sm.current = 'menu'
        return sm

if __name__ == '__main__':
    SwitchScreenApp().run()
