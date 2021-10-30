from flask import render_template, request, flash, redirect
from flask.helpers import url_for
import requests
from flask_login import login_required
from .import bp as main
from .forms import PokeNameForm

@main.route('/', methods=['GET'])
@login_required
def index():
    
    return render_template('home.html.j2')

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeNameForm()
    poke_list = requests.get("https://pokeapi.co/api/v2/pokemon/")
    if request.method == 'POST':
        names = request.form.get('name').strip(',').split(',')
        
        pokemon_info = []
        for name in names:
            name = name.strip(', ').lower()

            if ',' in name or name=="":
                flash('We could not find that entry in our database.', 'danger')
                return redirect(url_for('main.pokemon'))
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            if response.ok:
                #request worked
                if not response.json():
                    flash('We had an error loading your pokemon likely the name is not in the pokemon database','danger')
                    return redirect(url_for('main.pokemon'))
                pokemon = response.json()

                single_poke={
                    'name': pokemon['name'],
                    'base_xp': pokemon['base_experience'],
                    'hp': pokemon['stats'][0]['base_stat'],
                    'defense': pokemon['stats'][2]['base_stat'],
                    'attack': pokemon['stats'][1]['base_stat'],
                    'url': pokemon['sprites']['front_shiny']
                }
                pokemon_info.append(single_poke)

            
            else:
                flash('We could not find that entry in our database.', 'danger')
                return redirect(url_for('main.pokemon'))

        return render_template('pokemon.html.j2', pokemon=pokemon_info, form=form)     
        

    return render_template('pokemon.html.j2', form=form)