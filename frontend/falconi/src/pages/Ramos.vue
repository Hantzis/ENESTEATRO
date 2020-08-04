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
        <q-btn color="primary" style="margin-right: 12px;" @click="getRamos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevoramo = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Ramo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Ramos"
          :data.sync="datos_ramos"
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
              <q-btn dense round flat color="primary" @click="editRamoDialog(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="red" @click="deleteRamoDialog(props)" icon="delete"></q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoramo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Agregar nuevo ramo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del ramo" v-model="nuevo_ramo_nombre"
                       :error-message="mensaje_error" :error="ramonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 :disable="ramonuevo_invalido || !this.nuevo_ramo_nombre"
                 @click="addRamo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarramo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Editar ramo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del ramo" v-model="editar_ramo_nombre"
                       :error-message="mensaje_error" :error="ramonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar edición" color="primary" v-close-popup
                 :disable="ramomodificado_invalido || !this.editar_ramo_nombre"
                 @click="saveRamo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarramo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>¿Está seguro de eliminar este ramo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del ramo" v-model="eliminar_ramo_nombre"
                       :error-message="mensaje_error" :error="ramonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
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

export default {
  name: 'Ramos',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevoramo: false,
      dialogo_editarramo: false,
      dialogo_eliminarramo: false,
      nuevo_ramo_nombre: undefined,
      editar_ramo_nombre: undefined,
      editar_ramo_id: undefined,
      eliminar_ramo_nombre: undefined,
      eliminar_ramo_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Ramo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_ramos: [],
      noti: () => {
      },
    }
  },
  mounted() {
    this.getRamos()
  },
  methods: {
    async getRamos() {
      try {
        const resDB = await firebaseDB.collection('Ramo').get()
        this.datos_ramos = []
        resDB.forEach(res => {
          const ramo = {id: res.id, nombre: res.data().nombre}
          this.datos_ramos.push(ramo)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        console.log(error)
        this.tabla_loading = false
      }
    },
    async addRamo() {
      try {
        const resDB = await firebaseDB.collection('Ramo').add({nombre: this.nuevo_ramo_nombre})
        console.log(resDB.id)
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se agregó el nuevo ramo "${this.nuevo_ramo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.nuevo_ramo_nombre = undefined
        await this.getRamos()
      }
    },
    async saveRamo() {
      try {
        await firebaseDB.collection('Ramo').doc(
          this.editar_ramo_id).update({nombre: this.editar_ramo_nombre})
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se modifico el ramo "${this.editar_ramo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.editar_ramo_nombre = undefined
        this.editar_ramo_id = undefined
        await this.getRamos()
      }
    },
    async deleteRamo() {
      try {
        await firebaseDB.collection('Ramo').doc(this.eliminar_ramo_id).delete()
        this.$q.notify({
          type: 'negative',
          multiLine: true,
          message: `Se eliminó el ramo "${this.eliminar_ramo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.eliminar_ramo_nombre = undefined
        this.eliminar_ramo_id = undefined
        await this.getRamos()
      }
    },
    cancelar_guardado() {
      this.nuevo_ramo_nombre = undefined
      this.editar_ramo_nombre = undefined
    },
    editRamoDialog(props) {
      this.dialogo_editarramo = true
      this.editar_ramo_nombre = props.row.nombre
      this.editar_ramo_id = props.row.id
    },
    deleteRamoDialog(props) {
      this.dialogo_eliminarramo = true
      this.eliminar_ramo_nombre = props.row.nombre
      this.eliminar_ramo_id = props.row.id
    },
  },
  computed: {
    ramonuevo_invalido() {
      if (this.nuevo_ramo_nombre) {
        let existe = false;
        for (let item of this.datos_ramos) {
          if (item.nombre === this.nuevo_ramo_nombre) {
            existe = true
            console.log("existe")
          }
        }
        return this.nuevo_ramo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    ramomodificado_invalido() {
      if (this.editar_ramo_nombre) {
        let existe = false;
        for (let item of this.datos_ramos) {
          if (item.nombre === this.editar_ramo_nombre && item.nombre !== this.editar_ramo_id) {
            existe = true
            console.log("existe")
          }
        }
        return this.editar_ramo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of this.datos_ramos) {
        if (item.nombre === this.nuevo_ramo_nombre) {
          mensaje += "Ya existe un ramo con ese nombre. "
          console.log("existe")
        }
      }
      return mensaje
    }
  }
}
</script>
