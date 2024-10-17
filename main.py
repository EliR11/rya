import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
from datetime import datetime  # Importar datetime para manejar fechas

def get_total_personas():
    return Persona.query.count()

def get_total_por_ciudad():
    return db.session.query(Persona.ciudad, db.func.count(Persona.id)).group_by(Persona.ciudad).all()

def get_porcentaje_edades():
    edades = [persona.edad for persona in Persona.query.all()]
    grupos = Counter((edad // 10) * 10 for edad in edades)  # Agrupamos por decenas
    return dict(grupos)

app = Flask(__name__)

# Configuración de la base de datos SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    nro_acreditacion = db.Column(db.String(50), nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    copia_ci_actualizada = db.Column(db.String(100), nullable=True)
    certificado_salud_mental = db.Column(db.String(100), nullable=True)
    vencimiento_csm = db.Column(db.Date, nullable=True)
    credencial = db.Column(db.String(100), nullable=True)
    constancia_trabajo = db.Column(db.String(100), nullable=True)
    sintesis_curricular = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    ano_acreditacion = db.Column(db.Integer, nullable=False)
    nro_gaceta = db.Column(db.String(50), nullable=True)
    nro_decision = db.Column(db.String(50), nullable=True)
    activo_en_defensoria = db.Column(db.Boolean, default=False)
    direccion_defensoria = db.Column(db.String(150), nullable=True)
    inactivo = db.Column(db.Boolean, default=False)
    motivo = db.Column(db.String(255), nullable=True)
    trabaja_actualmente = db.Column(db.Boolean, default=False)
    lugar_trabajo = db.Column(db.String(100), nullable=True)

    # Campos para renovaciones y decisiones adicionales
    primera_fecha_renovacion = db.Column(db.Date, nullable=True)
    nro_gaceta2 = db.Column(db.String(50), nullable=True)
    nro_decision2 = db.Column(db.String(50), nullable=True)
    
    segunda_fecha_renovacion = db.Column(db.Date, nullable=True)
    nro_gaceta3 = db.Column(db.String(50), nullable=True)
    nro_decision3 = db.Column(db.String(50), nullable=True)

    tercera_fecha_renovacion = db.Column(db.Date, nullable=True)
    nro_gaceta4 = db.Column(db.String(50), nullable=True)
    nro_decision4 = db.Column(db.String(50), nullable=True)

    cuarta_fecha_renovacion = db.Column(db.Date, nullable=True)
    nro_gaceta5 = db.Column(db.String(50), nullable=True)
    nro_decision5 = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Persona {self.nombres} {self.apellidos}>'

# Rutas CRUD
@app.route('/')
def index():
    personas = Persona.query.all()
    return render_template('index.html', personas=personas)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        nro_acreditacion = request.form['nro_acreditacion']
        nacionalidad = request.form['nacionalidad']
        cedula = request.form['cedula']
        copia_ci_actualizada = request.form['copia_ci_actualizada']
        certificado_salud_mental = request.form['certificado_salud_mental']
        vencimiento_csm = request.form.get('vencimiento_csm')  # Convertir a tipo fecha
        if vencimiento_csm:
            vencimiento_csm = datetime.strptime(vencimiento_csm, '%Y-%m-%d').date()
        credencial = request.form['credencial']
        constancia_trabajo = request.form['constancia_trabajo']
        sintesis_curricular = request.form['sintesis_curricular']
        telefono = request.form['telefono']
        ano_acreditacion = request.form['ano_acreditacion']
        nro_gaceta = request.form['nro_gaceta']
        nro_decision = request.form['nro_decision']
        activo_en_defensoria = 'activo_en_defensoria' in request.form  # Checkbox
        direccion_defensoria = request.form['direccion_defensoria']
        inactivo = 'inactivo' in request.form  # Checkbox
        motivo = request.form['motivo']
        trabaja_actualmente = 'trabaja_actualmente' in request.form  # Checkbox
        lugar_trabajo = request.form['lugar_trabajo']

        # Fechas de renovación
        primera_fecha_renovacion = request.form.get('primera_fecha_renovacion')
        if primera_fecha_renovacion:
            primera_fecha_renovacion = datetime.strptime(primera_fecha_renovacion, '%Y-%m-%d').date()
        nro_gaceta2 = request.form.get('nro_gaceta2')
        nro_decision2 = request.form.get('nro_decision2')

        segunda_fecha_renovacion = request.form.get('segunda_fecha_renovacion')
        if segunda_fecha_renovacion:
            segunda_fecha_renovacion = datetime.strptime(segunda_fecha_renovacion, '%Y-%m-%d').date()
        nro_gaceta3 = request.form.get('nro_gaceta3')
        nro_decision3 = request.form.get('nro_decision3')

        tercera_fecha_renovacion = request.form.get('tercera_fecha_renovacion')
        if tercera_fecha_renovacion:
            tercera_fecha_renovacion = datetime.strptime(tercera_fecha_renovacion, '%Y-%m-%d').date()
        nro_gaceta4 = request.form.get('nro_gaceta4')
        nro_decision4 = request.form.get('nro_decision4')

        cuarta_fecha_renovacion = request.form.get('cuarta_fecha_renovacion')
        if cuarta_fecha_renovacion:
            cuarta_fecha_renovacion = datetime.strptime(cuarta_fecha_renovacion, '%Y-%m-%d').date()
        nro_gaceta5 = request.form.get('nro_gaceta5')
        nro_decision5 = request.form.get('nro_decision5')

        nueva_persona = Persona(
            nombres=nombres,
            apellidos=apellidos,
            nro_acreditacion=nro_acreditacion,
            nacionalidad=nacionalidad,
            cedula=cedula,
            copia_ci_actualizada=copia_ci_actualizada,
            certificado_salud_mental=certificado_salud_mental,
            vencimiento_csm=vencimiento_csm,
            credencial=credencial,
            constancia_trabajo=constancia_trabajo,
            sintesis_curricular=sintesis_curricular,
            telefono=telefono,
            ano_acreditacion=ano_acreditacion,
            nro_gaceta=nro_gaceta,
            nro_decision=nro_decision,
            activo_en_defensoria=activo_en_defensoria,
            direccion_defensoria=direccion_defensoria,
            inactivo=inactivo,
            motivo=motivo,
            trabaja_actualmente=trabaja_actualmente,
            lugar_trabajo=lugar_trabajo,
            primera_fecha_renovacion=primera_fecha_renovacion,
            nro_gaceta2=nro_gaceta2,
            nro_decision2=nro_decision2,
            segunda_fecha_renovacion=segunda_fecha_renovacion,
            nro_gaceta3=nro_gaceta3,
            nro_decision3=nro_decision3,
            tercera_fecha_renovacion=tercera_fecha_renovacion,
            nro_gaceta4=nro_gaceta4,
            nro_decision4=nro_decision4,
            cuarta_fecha_renovacion=cuarta_fecha_renovacion,
            nro_gaceta5=nro_gaceta5,
            nro_decision5=nro_decision5
        )
        
        # Agregar a la base de datos y confirmar cambios
        db.session.add(nueva_persona)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    persona = Persona.query.get_or_404(id)
    
    if request.method == 'POST':
        persona.nombres = request.form['nombres']
        persona.apellidos = request.form['apellidos']
        persona.nro_acreditacion = request.form['nro_acreditacion']
        persona.nacionalidad = request.form['nacionalidad']
        persona.cedula = request.form['cedula']
        persona.copia_ci_actualizada = request.form['copia_ci_actualizada']
        persona.certificado_salud_mental = request.form['certificado_salud_mental']
        
        # Convertir a tipo fecha si es necesario
        vencimiento_csm = request.form.get('vencimiento_csm')
        if vencimiento_csm:
            persona.vencimiento_csm = datetime.strptime(vencimiento_csm, '%Y-%m-%d').date()
        
        persona.credencial = request.form['credencial']
        persona.constancia_trabajo = request.form['constancia_trabajo']
        persona.sintesis_curricular = request.form['sintesis_curricular']
        persona.telefono = request.form['telefono']
        persona.ano_acreditacion = request.form['ano_acreditacion']
        persona.nro_gaceta = request.form['nro_gaceta']
        persona.nro_decision = request.form['nro_decision']
        persona.activo_en_defensoria = 'activo_en_defensoria' in request.form  # Checkbox
        persona.direccion_defensoria = request.form['direccion_defensoria']
        persona.inactivo = 'inactivo' in request.form  # Checkbox
        persona.motivo = request.form['motivo']
        persona.trabaja_actualmente = 'trabaja_actualmente' in request.form  # Checkbox
        persona.lugar_trabajo = request.form['lugar_trabajo']

        # Fechas de renovación
        primera_fecha_renovacion = request.form.get('primera_fecha_renovacion')
        if primera_fecha_renovacion:
            persona.primera_fecha_renovacion = datetime.strptime(primera_fecha_renovacion, '%Y-%m-%d').date()
        persona.nro_gaceta2 = request.form.get('nro_gaceta2')
        persona.nro_decision2 = request.form.get('nro_decision2')

        segunda_fecha_renovacion = request.form.get('segunda_fecha_renovacion')
        if segunda_fecha_renovacion:
            persona.segunda_fecha_renovacion = datetime.strptime(segunda_fecha_renovacion, '%Y-%m-%d').date()
        persona.nro_gaceta3 = request.form.get('nro_gaceta3')
        persona.nro_decision3 = request.form.get('nro_decision3')

        tercera_fecha_renovacion = request.form.get('tercera_fecha_renovacion')
        if tercera_fecha_renovacion:
            persona.tercera_fecha_renovacion = datetime.strptime(tercera_fecha_renovacion, '%Y-%m-%d').date()
        persona.nro_gaceta4 = request.form.get('nro_gaceta4')
        persona.nro_decision4 = request.form.get('nro_decision4')

        cuarta_fecha_renovacion = request.form.get('cuarta_fecha_renovacion')
        if cuarta_fecha_renovacion:
            persona.cuarta_fecha_renovacion = datetime.strptime(cuarta_fecha_renovacion, '%Y-%m-%d').date()
        persona.nro_gaceta5 = request.form.get('nro_gaceta5')
        persona.nro_decision5 = request.form.get('nro_decision5')

        # Confirmar cambios en la base de datos
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('update.html', persona=persona)

@app.route('/delete/<int:id>')
def delete(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/estadisticas')
def estadisticas():
    total_personas = get_total_personas()
    total_por_ciudad = get_total_por_ciudad()
    porcentaje_edades = get_porcentaje_edades()
    
    return render_template('estadisticas.html', 
                           total_personas=total_personas,
                           total_por_ciudad=total_por_ciudad,
                           porcentaje_edades=porcentaje_edades)

@app.route('/search', methods=['GET'])
def search():
    cedula = request.args.get('cedula')
    persona = Persona.query.filter_by(cedula=cedula).first()

    if persona:
        return render_template('detail.html', persona=persona)
    else:
        return render_template('not_found.html', cedula=cedula)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas
app.run(debug=True)  # Inicia el servidor en modo debug