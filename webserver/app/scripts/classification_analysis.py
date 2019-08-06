from bokeh.layouts import row
from bokeh.models import Panel, WidgetBox
from bokeh.models.widgets import TextAreaInput, RadioButtonGroup, Button, Paragraph
from joblib import load


def classification_tab():
    pairs = [["stackoverflow.com", "academia.stackexchange.com"],["stackoverflow.com", "softwareengineering.stackexchange.com"]]
    
    # pretrained classification models
    nbsoac = load("app/models/10k_so_ac_bayes_model.joblib")
    nbsose = load("app/models/10k_so_se_bayes_model.joblib")
    svmsoac = load("app/models/10k_so_ac_SVM_model.joblib")
    svmsose = load("app/models/10k_so_se_SVM_model.joblib")
    
    learning_type = RadioButtonGroup(labels=["Bayes", "Support Vector Machine"], active=0)
    
    site_pair = RadioButtonGroup(labels=["Stack Overflow/Academia", "Stack Overflow/Software Engineering"], active=0)
    
    tai = TextAreaInput(value="", rows=6, title="Enter a post message:")
    
    predict = Button(label="Predict", button_type="success")
    
    p = Paragraph(text="""Your Site Prediction will be displayed here""",
            width=300, height=50)
    
    def make_prediction():
        lt = learning_type.active
        sp = site_pair.active
        model = None
        if lt == 0:
            if sp == 0:
                model = nbsoac
            else:
                model = nbsose
        else:
            if sp == 0:
                model = svmsoac
            else:
                model = svmsose
        prediction = model.predict([tai.value])[0]
        p.text = "Message belongs to site: " + pairs[sp][prediction - 1]


    predict.on_click(make_prediction)

    # Put controls in a single element
    controls = WidgetBox(learning_type, site_pair, tai, predict, p)

    # Create a row layout
    layout = row(controls)

    tab = Panel(child=layout, title='Message Site Classification')

    return tab
