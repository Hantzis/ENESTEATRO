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
          :grid1="$q.screen.xs"
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
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Agregar nuevo archivo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del archivo" v-model="nuevo_archivo_nombre"
                       :error-message="mensaje_error" :error="archivonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 :disable="archivonuevo_invalido || !this.nuevo_archivo_nombre"
                 @click="addArchivo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editararchivo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Editar archivo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del archivo" v-model="editar_archivo_nombre"
                       :error-message="mensaje_error" :error="archivonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar edición" color="primary" v-close-popup
                 :disable="archivomodificado_invalido || !this.editar_archivo_nombre"
                 @click="saveArchivo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminararchivo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>¿Está seguro de eliminar este archivo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del archivo" v-model="eliminar_archivo_nombre"
                       :error-message="mensaje_error" :error="archivonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
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
      nuevo_archivo_nombre: undefined,
      editar_archivo_nombre: undefined,
      editar_archivo_id: undefined,
      eliminar_archivo_nombre: undefined,
      eliminar_archivo_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Archivo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_archivos: [],
      noti: () => {
      },
    }
  },
  mounted() {
    this.getArchivos()
  },
  methods: {
    async getArchivos() {
      try {
        const resDB = await firebaseDB.collection('Archivo').get()
        this.datos_archivos = []
        resDB.forEach(res => {
          const archivo = {id: res.id, nombre: res.data().nombre}
          this.datos_archivos.push(archivo)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        console.log(error)
        this.tabla_loading = false
      }
    },
    async addArchivo() {
      try {
        const resDB = await firebaseDB.collection('Archivo').add({nombre: this.nuevo_archivo_nombre})
        console.log(resDB.id)
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se agregó el nuevo archivo "${this.nuevo_archivo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.nuevo_archivo_nombre = undefined
        await this.getArchivos()
      }
    },
    async saveArchivo() {
      try {
        await firebaseDB.collection('Archivo').doc(
          this.editar_archivo_id).update({nombre: this.editar_archivo_nombre})
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se modifico el archivo "${this.editar_archivo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.editar_archivo_nombre = undefined
        this.editar_archivo_id = undefined
        await this.getArchivos()
      }
    },
    async deleteArchivo() {
      try {
        await firebaseDB.collection('Archivo').doc(this.eliminar_archivo_id).delete()
        this.$q.notify({
          type: 'negative',
          multiLine: true,
          message: `Se eliminó el archivo "${this.eliminar_archivo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.eliminar_archivo_nombre = undefined
        this.eliminar_archivo_id = undefined
        await this.getArchivos()
      }
    },
    cancelar_guardado() {
      this.nuevo_archivo_nombre = undefined
      this.editar_archivo_nombre = undefined
    },
    editArchivoDialog(props) {
      this.dialogo_editararchivo = true
      this.editar_archivo_nombre = props.row.nombre
      this.editar_archivo_id = props.row.id
    },
    deleteArchivoDialog(props) {
      this.dialogo_eliminararchivo = true
      this.eliminar_archivo_nombre = props.row.nombre
      this.eliminar_archivo_id = props.row.id
    },
  },
  computed: {
    archivonuevo_invalido() {
      if (this.nuevo_archivo_nombre) {
        let existe = false;
        for (let item of this.datos_archivos) {
          if (item.nombre === this.nuevo_archivo_nombre) {
            existe = true
            console.log("existe")
          }
        }
        return this.nuevo_archivo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    archivomodificado_invalido() {
      if (this.editar_archivo_nombre) {
        let existe = false;
        for (let item of this.datos_archivos) {
          if (item.nombre === this.editar_archivo_nombre && item.nombre !== this.editar_archivo_id) {
            existe = true
            console.log("existe")
          }
        }
        return this.editar_archivo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of this.datos_archivos) {
        if (item.nombre === this.nuevo_archivo_nombre) {
          mensaje += "Ya existe un archivo con ese nombre. "
          console.log("existe")
        }
      }
      return mensaje
    }
  }
}
</script>
