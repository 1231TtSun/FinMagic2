from . import index_prediction
from flask import render_template
@index_prediction.route('dpfx_dpzs/<code>',methods=['GET','POST'])
def dpfx_dpzs(code):
    return render_template('index_prediction/dpfx_dpzs.html',code = code)