from flask import Flask, render_template
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import BooleanField

import numpy as np
import pandas as pd

from .. import settings


class EvaluationServer(object):
    def __init__(self,
                 app_name,
                 evaluation_file_name,
                 samples,
                 template_dir=None,
                 batch_size=10,
                 host='localhost',
                 port=8080):
        self.app_name = app_name
        self.samples = samples
        self.evaluation_file_name = evaluation_file_name
        self.batch_size = batch_size
        self.host = host
        self.port = port
        self._curr_id = 0
        self.evaluations = np.zeros([samples.shape[0]]) - 1
        if template_dir is None:
            self.template_dir = settings.TEMPLATE_DIR
            print(self.template_dir)
        else:
            self.template_dir = template_dir

    def generate_evaluation_form(self):
        class EvalForm(Form):
            pass

        for i in range(self.samples.shape[0]):
            name = 'eval_%s' % i
            setattr(EvalForm,
                    name,
                    BooleanField(name))

        return EvalForm()

    def next_batch_or_exit(self):
        form = self.generate_evaluation_form()

        if form.validate_on_submit():
            for i in range(self.samples.shape[0]):
                self.evaluations[i] = getattr(form, 'eval_%s' % i).data
            of_name = 'curated_labels/%s' % self.evaluation_file_name
            pd.DataFrame(self.evaluations, index=self.samples.index).to_csv(of_name)
        rows = []
        for i, row in self.samples.iterrows():
            rows.append(row.tolist() + [getattr(form, 'eval_%s' % i)])
        return render_template('index.html',
                               samples=rows,
                               headers=self.samples.columns,
                               form=form)

    def run(self):
        app = Flask(self.app_name,
                    template_folder=self.template_dir)
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SECRET_KEY'] = 'thisisit'
        Bootstrap(app)

        app.debug = True
        app.add_url_rule('/',
                         'self.next_batch_or_exit',
                         self.next_batch_or_exit,
                         methods=('GET', 'POST'))
        app.run(host=self.host, port=self.port)
