import panel as pn
from dashapi import DASHAPI
import altair as alt
import datetime as dt

api = DASHAPI()
api.load_data("ds4200_project_co2_data.csv")
api.clean_data()

# Loads javascript dependencies and configures Panel (required)
pn.extension()


# search widgets

country = pn.widgets.Select(name="Country", options=api.get_countries(), value='World')
country_select = pn.widgets.MultiChoice(name='MultiChoice', value=['United States'],
                    options=api.get_countries())
gdp_range = pn.widgets.EditableRangeSlider(name='GDP (Billions)', start=0, end=27000, step=10)


# Plotting widgets

year = pn.widgets.EditableRangeSlider(name='Year', start=1990, end=2022, step=1)
width = pn.widgets.IntSlider(name="Width", start=250, end=850, step=50, value=650)
height = pn.widgets.IntSlider(name="Height", start=200, end=800, step=50, value=600)


# CALLBACK FUNCTIONS

def extract_countries(country, gdp_range, year):
    global source
    source = api.extract_countries(country, gdp_range, year)  # calling the api
    table = pn.widgets.Tabulator(source, selectable=False)
    return table




def get_gdp_plot(country, gdp_range, year, width, height):
    if (country == 'World'):
        # allowing altair to still plot despite how many rows there are
        alt.data_transformers.disable_max_rows()
        fig = alt.Chart(source).mark_line(point = True).encode(
            alt.X('year'),
            alt.Y('gdp').title("GDP (USD)"),
            color = "country",
            tooltip = ['country', 'gdp', 'year']

        ).transform_filter(alt.datum.country != 'World').properties(width = width, height = height).interactive()
    else:
        fig = alt.Chart(source).mark_line(point = True).encode(
            alt.X('year'),
            alt.Y('gdp').title("GDP (USD)"),
            color = 'country'
        ).transform_filter(alt.datum.country != 'World').properties(width = width, height = height).interactive()

    return fig

def get_gdp_filter_plot(country_select, year, width, height):
    alt.data_transformers.disable_max_rows()
    data = api.extract_filter_countries(country_select, year)
    fig = alt.Chart(data).mark_line(point=True).encode(
        alt.X('year'),
        alt.Y('gdp').title("GDP (USD)"),
        color="country",
        tooltip=['country', 'gdp', 'year']
    ).properties(width = width, height = height).interactive()

    return fig

# CALLBACK BINDINGS (Connecting widgets to callback functions)
catalog = pn.bind(extract_countries,country, gdp_range, year)
gdp_plot = pn.bind(get_gdp_plot, country, gdp_range, year, width, height)
gdp_filter_plot = pn.bind(get_gdp_filter_plot, country_select, year, width, height)




# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

country_card = pn.Card(
    pn.Column(
        country,
        gdp_range

    ),
    title="Country", width=card_width + 20, collapsed=False
)

country_select_card = pn.Card(
    pn.Column(
        country_select
    ),
    title = "Compare Countries", width=card_width + 20, collapsed=True
)

# editing altair plot visuals
plot_card = pn.Card(
    pn.Column(
        year,
        width,
        height
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="GDP of Various Countries Over Time",
    sidebar=[
        country_card,
        country_select_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Selected Data", catalog),
            ("GDP Over Time (Overall)", gdp_plot),
            ("GDP Over Time (Specified Comparison)", gdp_filter_plot),
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#a93226'

).servable()

layout.show()