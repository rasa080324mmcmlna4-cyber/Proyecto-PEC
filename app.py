from flask import Flask, render_template, request, redirect, session
from functools import wraps
import os  # Agregado para leer las variables de entorno de Railway

app = Flask(__name__)
app.secret_key = "PEC"

# ---------------- LOGIN ----------------

USUARIOS_SISTEMA = {
    "admin": {
        "password": "123456",
        "rol": "admin"
    },
    "usuario": {
        "password": "123456",
        "rol": "usuario"
    }
}

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorador

def solo_admin(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get("rol") != "admin":
            return redirect("/")
        return f(*args, **kwargs)
    return decorador

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        clave = request.form["clave"]
        password = request.form["password"]

        if clave in USUARIOS_SISTEMA:
            if password == USUARIOS_SISTEMA[clave]["password"]:
                session["usuario"] = clave
                session["rol"] = USUARIOS_SISTEMA[clave]["rol"]
                return redirect("/")

        error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- DATOS ----------------

usuarios = []
rutas = []
contactos = []
residuos = []
puntos = []
campanas = []
reportes = []

# ---------------- HOME ----------------

@app.route("/")
@login_requerido
def index():
    return render_template("index.html")

# ---------------- CONTACTOS ----------------

@app.route("/contactos")
@login_requerido
def contactos_page():
    return render_template("contactos.html", contactos=contactos)

@app.route("/guardar_contacto", methods=["POST"])
@login_requerido
def guardar_contacto():
    contactos.append({
        "nombre": request.form["nombre"],
        "telefono": request.form["telefono"],
        "mensaje": request.form["mensaje"]
    })
    return redirect("/contactos")

@app.route("/eliminar_contacto/<int:index>")
@login_requerido
def eliminar_contacto(index):
    contactos.pop(index)
    return redirect("/contactos")

# ---------------- RUTAS ----------------

@app.route("/rutas")
@login_requerido
@solo_admin
def rutas_page():
    return render_template("rutas.html", rutas=rutas)

@app.route("/guardar_ruta", methods=["POST"])
@login_requerido
@solo_admin
def guardar_ruta():
    rutas.append({
        "nombre": request.form["nombre"],
        "origen": request.form["origen"],
        "destino": request.form["destino"]
    })
    return redirect("/rutas")

@app.route("/eliminar_ruta/<int:index>")
@login_requerido
@solo_admin
def eliminar_ruta(index):
    rutas.pop(index)
    return redirect("/rutas")

@app.route("/editar_ruta/<int:index>")
@login_requerido
@solo_admin
def editar_ruta(index):
    return render_template("editar_ruta.html", r=rutas[index], index=index)

@app.route("/actualizar_ruta/<int:index>", methods=["POST"])
@login_requerido
@solo_admin
def actualizar_ruta(index):
    rutas[index] = {
        "nombre": request.form["nombre"],
        "origen": request.form["origen"],
        "destino": request.form["destino"]
    }
    return redirect("/rutas")

# ---------------- USUARIOS ----------------

@app.route("/usuarios")
@login_requerido
@solo_admin
def usuarios_page():
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/guardar_usuario", methods=["POST"])
@login_requerido
@solo_admin
def guardar_usuario():
    usuarios.append({
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "rol": request.form["rol"]
    })
    return redirect("/usuarios")

@app.route("/eliminar_usuario/<int:index>")
@login_requerido
@solo_admin
def eliminar_usuario(index):
    usuarios.pop(index)
    return redirect("/usuarios")

@app.route("/editar_usuario/<int:index>")
@login_requerido
@solo_admin
def editar_usuario(index):
    return render_template("editar_usuario.html", u=usuarios[index], index=index)

@app.route("/actualizar_usuario/<int:index>", methods=["POST"])
@login_requerido
@solo_admin
def actualizar_usuario(index):
    usuarios[index] = {
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "rol": request.form["rol"]
    }
    return redirect("/usuarios")

# ---------------- RESIDUOS ----------------

@app.route("/residuos")
@login_requerido
@solo_admin
def residuos_page():
    return render_template("residuos.html", residuos=residuos)

@app.route("/guardar_residuo", methods=["POST"])
@login_requerido
@solo_admin
def guardar_residuo():
    residuos.append({
        "tipo": request.form["tipo"],
        "cantidad": request.form["cantidad"]
    })
    return redirect("/residuos")

# ---------------- PUNTOS ----------------

@app.route("/puntos")
@login_requerido
@solo_admin
def puntos_page():
    return render_template("puntos.html", puntos=puntos)

@app.route("/guardar_punto", methods=["POST"])
@login_requerido
@solo_admin
def guardar_punto():
    puntos.append({
        "nombre": request.form["nombre"],
        "direccion": request.form["direccion"]
    })
    return redirect("/puntos")

# ---------------- CAMPAÑAS ----------------

@app.route("/campanas")
@login_requerido
@solo_admin
def campanas_page():
    return render_template("campanas.html", campanas=campanas)

@app.route("/guardar_campana", methods=["POST"])
@login_requerido
@solo_admin
def guardar_campana():
    campanas.append({
        "nombre": request.form["nombre"],
        "fecha": request.form["fecha"]
    })
    return redirect("/campanas")

# ---------------- REPORTES ----------------

@app.route("/reportes")
@login_requerido
def reportes_page():
    return render_template("reportes.html", reportes=reportes)

@app.route("/guardar_reporte", methods=["POST"])
@login_requerido
def guardar_reporte():
    reportes.append({
        "descripcion": request.form["descripcion"],
        "ubicacion": request.form["ubicacion"],
        "estado": "Pendiente"
    })
    return redirect("/reportes")

# ---------------- EJECUTAR ----------------

if __name__ == "__main__":
    # Lee el puerto que Railway le asigne al contenedor, o usa 5000 por defecto de forma local
    port = int(os.environ.get("PORT", 5000))
    # Escucha en todas las interfaces de red ('0.0.0.0') para que sea accesible públicamente
    app.run(host="0.0.0.0", port=port, debug=True)