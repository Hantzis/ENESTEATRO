<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Fondos" icon="inbox"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getFondos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn v-if="es_usuario && es_admin" style="margin-left: 8px;" color="green" @click="addFondoDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Fondo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Fondos"
          :data.sync="Object.values(datos_fondos)"
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
                <q-btn dense round flat color="primary" @click="editFondoDialog(props)" icon="edit"></q-btn>
                <q-btn dense round flat color="red" @click="deleteFondoDialog(props)" icon="delete"></q-btn>
              </div>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoarchivo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="green" text-color="white"/>
          <q-toolbar-title>Agregar nuevo archivo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del archivo" v-model="archivo_nombre"
                       :error-message="mensaje_error" :error="archivonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar" color="primary" v-close-popup
                 :disable="archivonuevo_invalido || !this.archivo_nombre"
                 @click="addFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editararchivo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="edit" color="primary" text-color="white"/>
          <q-toolbar-title>Editar archivo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del archivo" v-model="archivo_nombre"
                       :error-message="mensaje_error" :error="archivomodificado_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar" color="primary" v-close-popup
                 :disable="archivomodificado_invalido || !this.archivo_nombre"
                 @click="updateFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminararchivo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="red" text-color="white"/>
          <q-toolbar-title>Eliminar archivo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <p>¿Está seguro de eliminar este archivo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del archivo" v-model="archivo_nombre"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"
import firebase from "firebase";


export default {
  name: 'Fondos',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevoarchivo: false,
      dialogo_editararchivo: false,
      dialogo_eliminararchivo: false,
      archivo_nombre: undefined,
      archivo_nombre_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Fondo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_fondos: [],
      es_usuario: false,
      es_admin: false,
      firebaseRef: firebaseDB.collection('Fondo'),
    }
  },
  mounted() {
    this.getFondos()
  },
  created() {
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      if ((!(snapshot.docs.length === snapshot.docChanges().length) && snapshot.docChanges().length === 1)) {
        snapshot.docChanges().forEach(change => {
          this.getFondos()
          if (change.type === "added") {
            this.$q.notify({
              type: 'positive',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se agregó el nuevo archivo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "removed") {
            this.$q.notify({
              type: 'negative',
              multiLine: true,
              message: `Se eliminó el archivo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "modified") {
            this.$q.notify({
              type: 'info',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se modifico el archivo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          }
        })
      }
      this.archivo_nombre = undefined;
      this.archivo_id = undefined;
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
            console.log("ES ADMIN")
          } else {
            console.log("NO ES ADMIN")
          }
        })
      } else {
        this.es_usuario = false;
      }
    });
  },
  methods: {
    getFondos() {
      this.tabla_loading = true
      console.log("get fondos")
      this.firebaseRef.get().then(response => {
        this.datos_fondos = {}
        response.forEach(res => {
          this.datos_fondos[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
      })
    },
    addFondo() {
      this.tabla_loading = true
      this.firebaseRef.add({nombre: this.archivo_nombre})
      this.tabla_loading = false
    },
    updateFondo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.archivo_id).update({nombre: this.archivo_nombre})
      this.tabla_loading = false
    },
    deleteFondo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.archivo_id).delete()
      this.tabla_loading = false
    },
    cancelar_guardado() {
      this.archivo_nombre = undefined
      this.archivo_id = undefined
    },
    addFondoDialog() {
      this.dialogo_nuevoarchivo = true
    },
    editFondoDialog(props) {
      console.log(props)
      this.dialogo_editararchivo = true
      this.archivo_nombre = props.row.nombre
      this.archivo_id = props.row.id
    },
    deleteFondoDialog(props) {
      console.log(props)
      this.dialogo_eliminararchivo = true
      this.archivo_nombre = props.row.nombre
      this.archivo_id = props.row.id
    },
  },
  computed: {
    archivonuevo_invalido() {
      if (this.archivo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_fondos)) {
          if (item.nombre === this.archivo_nombre) {
            existe = true
          }
        }
        return this.archivo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    archivomodificado_invalido() {
      if (this.archivo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_fondos)) {
          if (item.nombre === this.archivo_nombre && item.id !== this.archivo_id) {
            existe = true
          }
        }
        return this.archivo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of Object.values(this.datos_fondos)) {
        if (item.nombre === this.archivo_nombre) {
          mensaje += "Ya existe un archivo con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
