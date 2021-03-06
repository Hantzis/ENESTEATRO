<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Lugares" icon="place"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getLugares()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn v-if="es_usuario" style="margin-left: 8px;" color="green" @click="addLugarDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Lugar</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Lugares"
          :data.sync="Object.values(datos_lugares)"
          :columns="columns"
          row-key="id"
          :loading="tabla_loading"
          :filter="filter"
        >
          <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div v-if="es_usuario && es_admin">
                <q-btn dense round flat color="primary" @click="editLugarDialog(props)" icon="edit"></q-btn>
                <q-btn dense round flat color="red" @click="deleteLugarDialog(props)" icon="delete"></q-btn>
              </div>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevolugar" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="green" text-color="white"/>
          <q-toolbar-title>Agregar nuevo lugar</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del lugar" v-model="lugar_nombre"
                       :error-message="mensaje_error" :error="lugarnuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar" color="primary" v-close-popup
                 :disable="lugarnuevo_invalido || !this.lugar_nombre"
                 @click="addLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarlugar" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="edit" color="primary" text-color="white"/>
          <q-toolbar-title>Editar lugar</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del lugar" v-model="lugar_nombre"
                       :error-message="mensaje_error" :error="lugarmodificado_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar" color="primary" v-close-popup
                 :disable="lugarmodificado_invalido || !this.lugar_nombre"
                 @click="updateLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarlugar" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="red" text-color="white"/>
          <q-toolbar-title>Eliminar lugar</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <p>¿Está seguro de eliminar este lugar?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del lugar" v-model="lugar_nombre"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"
import firebase from "firebase";


export default {
  name: 'Lugares',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevolugar: false,
      dialogo_editarlugar: false,
      dialogo_eliminarlugar: false,
      lugar_nombre: undefined,
      lugar_nombre_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Lugar', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_lugares: [],
      es_usuario: false,
      es_admin: false,
      firebaseRef: firebaseDB.collection('Lugar'),
    }
  },
  mounted() {
    this.getLugares()
  },
  created() {
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      if ((!(snapshot.docs.length === snapshot.docChanges().length) && snapshot.docChanges().length === 1)) {
        snapshot.docChanges().forEach(change => {
          this.getLugares()
          if (change.type === "added") {
            this.$q.notify({
              type: 'positive',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se agregó el nuevo lugar "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "removed") {
            this.$q.notify({
              type: 'negative',
              multiLine: true,
              message: `Se eliminó el lugar "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "modified") {
            this.$q.notify({
              type: 'info',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se modifico el lugar "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          }
        })
      }
      this.lugar_nombre = undefined;
      this.lugar_id = undefined;
      this.tabla_loading = false
    }, error => {
      console.log("error", error)
    }, () => {
      console.log("Complete")
    })
  },
  beforeCreate() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        this.es_usuario = true;
        firebaseDB.collection('Config').doc('usuarios').get().then(resDB => {
          if (resDB.data().admin.some(x => x === user.email)) {
            this.es_admin = true
          }
        }).catch(() => { })
      } else {
        this.es_usuario = false;
      }
    });
  },
  methods: {
    getLugares() {
      this.tabla_loading = true
      console.log("get lugares")
      this.firebaseRef.get().then(response => {
        this.datos_lugares = {}
        response.forEach(res => {
          this.datos_lugares[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(() => { }).finally(() => {
        this.tabla_loading = false
      })
    },
    addLugar() {
      this.tabla_loading = true
      this.firebaseRef.add({nombre: this.lugar_nombre})
      this.tabla_loading = false
    },
    updateLugar() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.lugar_id).update({nombre: this.lugar_nombre})
      this.tabla_loading = false
    },
    deleteLugar() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.lugar_id).delete()
      this.tabla_loading = false
    },
    cancelar_guardado() {
      this.lugar_nombre = undefined
      this.lugar_id = undefined
    },
    addLugarDialog() {
      this.dialogo_nuevolugar = true
    },
    editLugarDialog(props) {
      console.log(props)
      this.dialogo_editarlugar = true
      this.lugar_nombre = props.row.nombre
      this.lugar_id = props.row.id
    },
    deleteLugarDialog(props) {
      console.log(props)
      this.dialogo_eliminarlugar = true
      this.lugar_nombre = props.row.nombre
      this.lugar_id = props.row.id
    },
  },
  computed: {
    lugarnuevo_invalido() {
      if (this.lugar_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_lugares)) {
          if (item.nombre === this.lugar_nombre) {
            existe = true
          }
        }
        return this.lugar_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    lugarmodificado_invalido() {
      if (this.lugar_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_lugares)) {
          if (item.nombre === this.lugar_nombre && item.id !== this.lugar_id) {
            existe = true
          }
        }
        return this.lugar_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of Object.values(this.datos_lugares)) {
        if (item.nombre === this.lugar_nombre) {
          mensaje += "Ya existe un lugar con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
