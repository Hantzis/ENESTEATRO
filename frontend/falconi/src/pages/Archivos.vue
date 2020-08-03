<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Archivos" icon="drafts"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" style="margin-right: 12px;" @click="getArchivos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevoarchivo = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Archivo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Archivos"
          :data.sync="datos_archivos"
          :columns="columns"
          row-key="id"
          :grid="$q.screen.xs"
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
              <q-btn dense round flat color="grey" @click="editRow(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="grey" @click="deleteRow(props)" icon="delete"></q-btn>
            </q-td>
          </template>

        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoarchivo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Agregar nuevo archivo.</p>
          </div>

          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del archivo" v-model="archivo_nombre"
                       :error-message="mensaje_error" :error="archivo_invalido" />
            </div>
          </div>

        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_nuevoarchivo()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup :disable="archivo_invalido || !this.archivo_nombre"
                 @click="agregar_nuevoarchivo()"/>
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
      archivo_nombre: undefined,
      filas_productos_esvalido: false,
      columns: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {name: 'nombre', align: 'left', label: 'Nombre de Archivo', field: 'nombre', sortable: true},
        {name: 'actions', label: 'Actions', field: '', align: 'center'},
      ],
      datos_archivos: [],
      noti: () => {
      },
    }
  },
  mounted() {
    // get initial data from server (1st page)
    /*this.onRequest({
      pagination: this.pagination,
      filter: undefined
    })*/

    this.getArchivos()


  },
  methods: {
    async getArchivos() {
      this.tabla_loading = true
      const datos = this.datos_archivos
      try {
        const resDB = await firebaseDB.collection('Archivo').get()
        this.datos_archivos = []
        resDB.forEach(res => {
          console.log("res: ", res.data())
          const archivo = {id: res.id, nombre: res.data().nombre}
          this.datos_archivos.push(archivo)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        this.datos_archivos = datos
        console.log(error)
        this.tabla_loading = false
      }
    },
    async addArchivo() {
      const datos = this.datos_archivos
      try {
        const resDB = await firebaseDB.collection('Archivo').get()
        this.datos_archivos = []
        resDB.forEach(res => {
          console.log("res: ", res.data())
          const archivo = {id: res.id, nombre: res.data().nombre}
          this.datos_archivos.push(archivo)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        this.datos_archivos = datos
        console.log(error)
      }
    },
    cancelar_nuevoarchivo() {
      this.archivo_nombre = undefined
    },
    agregar_nuevoarchivo() {

    },
    editRow(props) {
      this.$q.notify({
        type: 'info',
        textColor: 'grey-10',
        multiLine: true,
        message: `I'll edit row data => ${JSON.stringify(props.row).split(',').join(', ')}`,
        timeout: 2000
      })
    },
    deleteRow(props) {
      this.noti()
      // do something
      this.noti = this.$q.notify({
        type: 'negative',
        multiline: true,
        message: `I'll delete row data => ${JSON.stringify(props.row).split(',').join(', ')}`,
        timeout: 2000
      })
    },

  },
  computed: {
    archivo_invalido() {
      if (this.archivo_nombre) {
        let existe = false;
        for (let item of this.datos_archivos) {
          if (item.nombre === this.archivo_nombre) {
            existe = true
            console.log("existe")
          }
        }
        return this.archivo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of this.datos_archivos) {
        if (item.nombre === this.archivo_nombre) {
          mensaje += "Ya existe un arhivo con ese nombre. "
          console.log("existe")
        }
      }
      return mensaje
    }
  }
}
</script>
