<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Archivos" icon="mdi-semantic-web"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" style="margin-right: 12px;" @click="getArchivos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="addArchivoDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Archivo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Archivos"
          :data.sync="Object.values(datos_archivos)"
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
              <q-btn dense round flat color="primary" @click="editArchivoDialog(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="red" @click="deleteArchivoDialog(props)" icon="delete"></q-btn>
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
                 @click="addArchivo()"/>
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
                 @click="updateArchivo()"/>
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
                 @click="deleteArchivo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"


export default {
  name: 'Archivos',
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
        {name: 'nombre', align: 'left', label: 'Nombre de Archivo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_archivos: [],
      firebaseRef: firebaseDB.collection('Archivo'),
    }
  },
  mounted() {
    this.getArchivos()
  },
  created() {
    this.tabla_loading = true
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      console.log("snap", snapshot)
      console.log("fromCache", snapshot.metadata.fromCache)
      console.log("docs", snapshot.docs)
      console.log("docs", snapshot.docs.length)
      console.log("DOCCHANGE: ", snapshot.docChanges())
      if (!((snapshot.docs.length == snapshot.docChanges().length) && snapshot.docChanges().length > 1)) {
        snapshot.docChanges().forEach(change => {
          console.log("change", change)
          console.log("change type", change.type)
          console.log("doc id", change.doc.id)
          console.log("doc data", change.doc.data())
          this.getArchivos()
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
      this.tabla_loading = false
    }, error => {
      console.log("error", error)
    }, () => {
      console.log("Al final!")
    })
    this.tabla_loading = false
  },
  methods: {
    getArchivos1() {
      console.log("get archivos")
      this.tabla_loading = true
      this.firebaseRef.get().then(response => {
        this.datos_archivos = {}
        response.forEach(res => {
          this.datos_archivos[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
        // console.log("DATOS ARCHIVOS: ", this.datos_archivos)
      })
    },
    getArchivos() {
      console.log("get archivos")
      this.tabla_loading = true
      this.firebaseRef.get().then(response => {
        this.datos_archivos = {}
        response.forEach(res => {
          this.datos_archivos[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
      })
    },
    addArchivo() {
      this.tabla_loading = true
      const add = this.firebaseRef.add({nombre: this.archivo_nombre})
      console.log("ADD", add)
      this.tabla_loading = false
    },
    updateArchivo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.archivo_id).update({nombre: this.archivo_nombre})
      this.tabla_loading = false
    },
    deleteArchivo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.archivo_id).delete()
      this.tabla_loading = false
    },
    cancelar_guardado() {
      this.archivo_nombre = undefined
      this.archivo_id = undefined
    },
    addArchivoDialog() {
      this.dialogo_nuevoarchivo = true
    },
    editArchivoDialog(props) {
      console.log(props)
      this.dialogo_editararchivo = true
      this.archivo_nombre = props.row.nombre
      this.archivo_id = props.row.id
    },
    deleteArchivoDialog(props) {
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
        for (let item of Object.values(this.datos_archivos)) {
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
        for (let item of Object.values(this.datos_archivos)) {
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
      for (let item of Object.values(this.datos_archivos)) {
        if (item.nombre === this.archivo_nombre) {
          mensaje += "Ya existe un archivo con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
