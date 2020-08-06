<template>
  <q-layout view="lhh lpR fFf">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="leftDrawer = !leftDrawer"/>
        <q-toolbar-title>
          Los Falconi
        </q-toolbar-title>
        <!-- {{ todaysDate }}&nbsp;&nbsp;&nbsp; -->
        <q-btn dense round flat @click="open_dialog_info = true" icon="info">
          <q-tooltip content-class="bg-amber text-black shadow-4" self="bottom right" anchor="center left" content-style="font-size: 16px">
            Info
          </q-tooltip>
        </q-btn>
        <q-btn v-if="!es_usuario" dense round flat @click="open_dialog_login = true" icon="login">
          <q-tooltip content-class="bg-amber text-black shadow-4" self="bottom right" anchor="center left" content-style="font-size: 16px">
            Iniciar sesión
          </q-tooltip>
        </q-btn>
        <q-btn v-if="es_usuario" dense round flat @click="open_dialog_logout = true" icon="logout">
          <q-tooltip content-class="bg-amber text-black shadow-4" self="bottom right" anchor="center left" content-style="font-size: 16px">
            Cerrar sesión
          </q-tooltip>
        </q-btn>
      </q-toolbar>
      <!-- <q-tabs align="right">
        <q-route-tab to="" label="Uno"/>
        <q-route-tab to="" label="Dos"/>
        <q-route-tab to="" label="Tres"/>
      </q-tabs> -->
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      :breakpoint="400"
    >
      <q-scroll-area style="height: calc(100% - 142px); margin-top: 142px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item to="/" clickable v-ripple exact>
            <q-item-section avatar>
              <q-icon name="home"/>
            </q-item-section>

            <q-item-section>
              Inicio
            </q-item-section>

          </q-item>
          <q-item to="registros" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-file-edit"/>
            </q-item-section>

            <q-item-section>
              Registros
            </q-item-section>
          </q-item>

          <q-separator></q-separator>

          <q-item to="archivos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-semantic-web"/>
            </q-item-section>
            <q-item-section>
              Archivos
            </q-item-section>
          </q-item>

          <q-item to="fondos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="inbox"/>
            </q-item-section>

            <q-item-section>
              Fondos
            </q-item-section>
          </q-item>

          <q-item to="lugares" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="place"/>
            </q-item-section>

            <q-item-section>
              Lugares
            </q-item-section>
          </q-item>

          <q-item to="ramos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-source-repository"/>
            </q-item-section>

            <q-item-section>
              Ramos
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar('mathereall@gmail.com', 150)">
          </q-avatar>
          <div class="text-weight-bold">César Benjamín García Martínez</div>
          <div>mathereall@gmail.com</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <keep-alive>
        <router-view/>
      </keep-alive>
    </q-page-container>

    <q-footer elevated class="bg-black text-grey-4">
      <q-toolbar style="min-height: 30px;">
        <q-toolbar-title style="font-size: 12px;">
          2020 &copy; UDIR - ENES Morelia
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

    <q-dialog v-model="open_dialog_info" persistent>
      <q-card style="width: 1000px; max-width: 80vw;">
        <q-card-section>
          <q-toolbar>
            <q-avatar>
              <img src="~assets/logo_udir.png">
            </q-avatar>
            <q-toolbar-title>Novísima compañía de teatro popular novohispano <span class="text-weight-bold">"Los Falconi"</span>
            </q-toolbar-title>
            <q-btn flat round dense icon="close" v-close-popup/>
          </q-toolbar>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <p>La Novísima compañía de teatro popular novohispano "Los Falconi" es un proyecto de la Licenciatura en
            Literatura Intercultural (UNAM, ENES Morelia).</p>
          <p>Los Falconi se dedican a crear, desde la dramaturgia al montaje, obras teatrales basadas en la
            investigación de archivo sobre las manifestaciones teatrales del siglo XVIII en la Nueva España. El proyecto
            es abierto a la participación tanto de la comunidad UNAM como del público en general. Presentaciones anuales
            cada mes de mayo. Pueden ver las obras pasadas en nuestro canal de YouTube, y próximamente tendremos a la
            venta (¡tiraje limitado!) las ediciones impresas de los libretos.</p>
          <p>La materia de Teatro Popular Novohispano forma parte del plan de estudios de la Licenciatura en Literatura
            Intercultural, que se imparte en la ENES Morelia. Desde 2016, año en que se comenzó a impartir, se llevado a
            cabo un ejercicio creativo: escribir, producir y montar una obra teatral a partir de los casos revisados,
            procedentes de fuentes documentales de archivos. Se ha puesto en marcha una experiencia de
            enseñanza-aprendizaje que, en los cuatro años de experiencia que lleva al momento de redactar estas líneas,
            ha demostrado ser muy provechosa para los alumnos; el beneficio ha redundado además en difusión cultural
            para la comunidad interna UNAM y para el público en general, siendo un excelente vehículo para transmitir de
            forma lúdica contenidos de interés histórico y académico.</p>
          <p>El planteamiento de la materia de Teatro Popular Novohispano nace de la inquietud por que, amén del
            análisis y crítica de textos literarios, de la historia e historiografía de la literatura, los alumnos se
            involucren en procesos creativos, por un lado, y gestionales, por el otro – una inquietud que caracteriza en
            su conjunto el enfoque de la Licenciatura en Literatura Intercultural que se imparte en la ENES Morelia. El
            hecho de que el proceso en cuestión sea la creación y montaje de una obra teatral (además de la edición y
            publicación de la misma) es especialmente relevante para la Licenciatura en Literatura Intercultural, por la
            importancia que en dicha licenciatura reviste la línea de investigación y área terminal de Artes Verbales,
            siendo el teatro justamente una de dichas artes: un interesante espacio de hibridación entre lo oral, lo
            escrito, lo visual y lo gestual.</p>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog v-model="open_dialog_login">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Iniciar sesión</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row">
            <div class="col">
              <div class="row">
                <div class="col" style="min-width: 256px;">
                  <q-form>
                    <div class="row">
                      <q-input class="full-width" name="email"
                               :rules="[val => !!val || 'Falta dirección de correo', isValidEmail]"
                               v-model="login_email" label="Dirección de correo"/>
                    </div>
                    <div class="row">
                      <q-input class="full-width" name="password" v-model="login_password" type="password"
                               label="Contraseña"/>
                    </div>
                    <br/>
                    <div class="row">
                      <div class="col" align="right">
                        <q-btn :disabled="!login_email || !login_password" @click="login()" color="green"
                               label="Ingresar" class="full-width"/>
                      </div>
                    </div>
                    <div class="row">
                      <p style="margin-bottom: 0px; margin-top: 10px;">{{ login_message }}</p>
                    </div>
                  </q-form>
                </div>
              </div>
              <div class="row">
                <div class="col q-pt-sm">
                  <div class="row q-py-sm">
                    <q-separator style="border-top: 1px dashed; background: white !important;;" color="green"/>
                  </div>
                  <div class="row">
                    <div class="col" align="right">
                      <p style="margin: 0"><a href="">Olvidé mi contraseña</a></p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn label="Cancelar" color="grey-10" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="open_dialog_logout">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="red" text-color="white"/>
          <q-toolbar-title>Cerrar sesión</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row">
            <div class="col">
              <div class="row">
                <div class="col" style="min-width: 256px;">
                    <div class="row">
                      <div class="col" align="right">
                        <q-btn @click="logout()" color="black"
                               label="Salir" class="full-width"/>
                      </div>
                    </div>
                    <div class="row">
                      <p style="margin-bottom: 0px; margin-top: 10px;">{{ login_message }}</p>
                    </div>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn label="Cancelar" color="black" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-layout>

</template>

<script>
import {date} from 'quasar'
import md5 from 'crypto-md5';
import firebase from 'firebase'

export default {
  data() {
    return {
      leftDrawer: false,
      open_dialog_info: false,
      open_dialog_login: false,
      open_dialog_logout: false,
      login_email: undefined,
      login_password: undefined,
      login_message: "",
      es_usuario: false
    }
  },
  computed: {
    todaysDate() {
      let timeStamp = Date.now()
      return date.formatDate(timeStamp, 'YYYY-MM-DD')
    }
  },
  watch: {
    login_email() {
      this.login_message = ""
    }
  },
  methods: {
    isValidEmail(val) {
      const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return emailPattern.test(val) || 'La dirección email no tiene formato correcto.';
    },
    get_gravatar(email, argsize) {
      const size = argsize
      return 'https://www.gravatar.com/avatar/' + md5(email.trim().toLowerCase(), 'hex') + '.jpg?s=' + size;
    },
    login() {
      firebase.auth().signInWithEmailAndPassword(this.login_email, this.login_password).then(response => {
        console.log(response)
        if (response.operationType === "signIn") {
          this.login_message = "Bienvenido."
          setTimeout(() => {
            this.open_dialog_login = false
            this.login_message = ""
            this.es_usuario = true
            this.login_email = undefined
            this.login_password = undefined
          }, 100)
        }
      }).catch(error => {
        console.log(error)
        if (error.code === "auth/invalid-email") {
          this.login_message = "La dirección email no tiene formato correcto."
        }
        if (error.code === "auth/user-not-found" || error.code === "auth/wrong-password") {
          this.login_message = "Usuario o contraeña incorrectos."
        }
      })
    },
    logout() {
      firebase.auth().signOut().then(response => {
        this.login_message = "Adios."
        setTimeout(() => {
            this.open_dialog_logout = false
            this.login_message = ""
            this.es_usuario = false
          }, 100)
      }).catch(error => {
        console.log(error)
      })
    },
  }
}
</script>
