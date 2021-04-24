
#
#Para TEST UNITARIOS
#
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

#
#Para manejo de errores
#
@app.errorhandler(500)
def server_error(error):
    context = {
        'admin' : session['admin'],
    }
    return render_template('400.html', error=error, **context)

    
@app.errorhandler(404)
def error(error):
    context={}
    if session.get('admin'):
        context['admin']= session['admin']
    return render_template('404.html', error=error, **context)





@app.route('/qrcode')
def qrcode():
    pass



