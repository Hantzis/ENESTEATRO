<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Ramos" icon="drafts"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getRamos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn v-if="es_usuario" style="margin-left: 8px;" color="green" @click="addRamoDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Ramo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Ramos"
          :data.sync="Object.values(datos_ramos)"
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
                <q-btn dense round flat color="primary" @click="editRamoDialog(props)" icon="edit"></q-btn>
                <q-btn dense round flat color="red" @click="deleteRamoDialog(props)" icon="delete"></q-btn>
              </div>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoramo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="green" text-color="white"/>
          <q-toolbar-title>Agregar nuevo ramo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del ramo" v-model="ramo_nombre"
                       :error-message="mensaje_error" :error="ramonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar" color="primary" v-close-popup
                 :disable="ramonuevo_invalido || !this.ramo_nombre"
                 @click="addRamo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarramo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="edit" color="primary" text-color="white"/>
          <q-toolbar-title>Editar ramo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del ramo" v-model="ramo_nombre"
                       :error-message="mensaje_error" :error="ramomodificado_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar" color="primary" v-close-popup
                 :disable="ramomodificado_invalido || !this.ramo_nombre"
                 @click="updateRamo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarramo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="red" text-color="white"/>
          <q-toolbar-title>Eliminar ramo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <p>¿Está seguro de eliminar este ramo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del ramo" v-model="ramo_nombre"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteRamo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"
import firebase from "firebase";


export default {
  name: 'Ramos',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevoramo: false,
      dialogo_editarramo: false,
      dialogo_eliminarramo: false,
      ramo_nombre: undefined,
      ramo_nombre_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Ramo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_ramos: [],
      es_usuario: false,
      es_admin: false,
      firebaseRef: firebaseDB.collection('Ramo'),
    }
  },
  mounted() {
    this.getRamos()
  },
  created() {
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      if ((!(snapshot.docs.length === snapshot.docChanges().length) && snapshot.docChanges().length === 1)) {
        snapshot.docChanges().forEach(change => {
          this.getRamos()
          if (change.type === "added") {
            this.$q.notify({
              type: 'positive',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se agregó el nuevo ramo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "removed") {
            this.$q.notify({
              type: 'negative',
              multiLine: true,
              message: `Se eliminó el ramo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "modified") {
            this.$q.notify({
              type: 'info',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se modifico el ramo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          }
        })
      }
      this.ramo_nombre = undefined;
      this.ramo_id = undefined;
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
    getRamos() {
      this.tabla_loading = true
      console.log("get ramos")
      this.firebaseRef.get().then(response => {
        this.datos_ramos = {}
        response.forEach(res => {
          this.datos_ramos[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(() => { }).finally(() => {
        this.tabla_loading = false
      })
    },
    addRamo() {
      this.tabla_loading = true
      this.firebaseRef.add({nombre: this.ramo_nombre})
      this.tabla_loading = false
    },
    updateRamo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.ramo_id).update({nombre: this.ramo_nombre})
      this.tabla_loading = false
    },
    deleteRamo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.ramo_id).delete()
      this.tabla_loading = false
    },
    cancelar_guardado() {
      this.ramo_nombre = undefined
      this.ramo_id = undefined
    },
    addRamoDialog() {
      this.dialogo_nuevoramo = true
    },
    editRamoDialog(props) {
      console.log(props)
      this.dialogo_editarramo = true
      this.ramo_nombre = props.row.nombre
      this.ramo_id = props.row.id
    },
    deleteRamoDialog(props) {
      console.log(props)
      this.dialogo_eliminarramo = true
      this.ramo_nombre = props.row.nombre
      this.ramo_id = props.row.id
    },
  },
  computed: {
    ramonuevo_invalido() {
      if (this.ramo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_ramos)) {
          if (item.nombre === this.ramo_nombre) {
            existe = true
          }
        }
        return this.ramo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    ramomodificado_invalido() {
      if (this.ramo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_ramos)) {
          if (item.nombre === this.ramo_nombre && item.id !== this.ramo_id) {
            existe = true
          }
        }
        return this.ramo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of Object.values(this.datos_ramos)) {
        if (item.nombre === this.ramo_nombre) {
          mensaje += "Ya existe un ramo con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
