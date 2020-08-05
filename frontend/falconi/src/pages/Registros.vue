<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Registros" icon="mdi-semantic-web"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" style="margin-right: 12px;" @click="getRegistros()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevoregistro = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Registro</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Registros"
          :data.sync="datos_registros"
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
              <q-btn dense round flat color="accent" @click="editRegistroDialog(props)" icon="mdi-plus"></q-btn>
              <q-btn dense round flat color="primary" @click="editRegistroDialog(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="red" @click="deleteRegistroDialog(props)" icon="delete"></q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoregistro" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">Agregar nuevo registro</div>
        </q-card-section>
        <q-card-section style="max-height: 50vh" class="scroll">
          <div class="row" >
            <div class="col">
              <q-select />
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
              <q-input name="nombre" label="Nombre del registro" v-model="nuevo_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 :disable="registronuevo_invalido || !this.nuevo_registro_nombre"
                 @click="addRegistro()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarregistro" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Editar registro</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del registro" v-model="editar_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar edición" color="primary" v-close-popup
                 :disable="registromodificado_invalido || !this.editar_registro_nombre"
                 @click="saveRegistro()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarregistro" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>¿Está seguro de eliminar este registro?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del registro" v-model="eliminar_registro_nombre"
                       :error-message="mensaje_error" :error="registronuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteRegistro()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
  import firebaseDB from "boot/firebase"

  export default {
    name: 'Registros',
    data() {
      return {
        filter: '',
        tabla_loading: false,
        dialogo_nuevoregistro: false,
        dialogo_editarregistro: false,
        dialogo_eliminarregistro: false,
        nuevo_registro_nombre: undefined,
        nuevo_registro_archivo: undefined,
        nuevo_registro_fondo: undefined,
        nuevo_registro_libro: undefined,
        nuevo_registro_foja: undefined,
        nuevo_registro_anos: undefined,
        nuevo_registro_lugar: undefined,
        nuevo_registro_ramo: undefined,
        nuevo_registro_encabezados: undefined,
        nuevo_registro_notas: undefined,
        nuevo_registro_transcripcion: undefined,
        nuevo_registro_usuario: undefined,
        editar_registro_nombre: undefined,
        editar_registro: undefined,
        editar_registro_id: undefined,
        eliminar_registro_nombre: undefined,
        eliminar_registro_id: undefined,
        columns: [
          {name: 'archivo', align: 'left', label: 'Archivo', field: 'archivo', sortable: true},
          {name: 'fondo', align: 'left', label: 'Fondo', field: 'fondo', sortable: true},
          {name: 'libro', align: 'left', label: 'Libro', field: 'libro', sortable: true},
          {name: 'foja', align: 'left', label: 'Foja', field: 'foja', sortable: true},
          {name: 'años', align: 'left', label: 'Años', field: 'años', sortable: true},
          {name: 'lugar', align: 'left', label: 'Lugar', field: 'lugar', sortable: true},
          {name: 'ramo', align: 'left', label: 'Ramo', field: 'ramo', sortable: true},
          {name: 'encabezados', align: 'left', label: 'Encabezados', field: 'encabezados', sortable: true},
          {name: 'notas', align: 'left', label: 'Notas', field: 'notas', sortable: true},
          {name: 'transcripcion', align: 'left', label: 'Transcripción', field: 'transcripcion', sortable: true},
          {name: 'usuario', align: 'left', label: 'Usuario', field: 'usuario', sortable: true},

          {name: 'actions', label: '', field: 'actions', align: 'right'},
        ],
        datos_registros: [],
        noti: () => {
        },
      }
    },
    mounted() {
      this.getRegistros()
    },
    methods: {
      getRegistros() {
        firebaseDB.collection('Registro').get().then(resDB => {
          this.datos_registros = [];
          resDB.forEach(res => {
            let years = "";
            if (res.data().años) {
              years = res.data().años.join(", ")
            }
            const registro = {id: res.id,
              archivo: res.data().archivo,
              fondo: res.data().fondo,
              libro: res.data().libro,
              foja: res.data().foja,
              años: years,
              lugar: res.data().lugar,
              ramo: res.data().ramo,
              encabezados: res.data().encabezados,
              notas: res.data().notas,
              transcripcion: res.data().transcripcion,
              usuario: res.data().usuario,
            };
            console.log(res.data().años)
            this.datos_registros.push(registro);
          });
          console.log("registros: ", this.datos_registros);
          this.tabla_loading = false
        }).catch(error => {
          console.log(error);
          this.tabla_loading = false;
        })
      },
      async addRegistro() {
        try {
          const resDB = await firebaseDB.collection('Registro').add({nombre: this.nuevo_registro_nombre})
          console.log(resDB.id)
          this.$q.notify({
            type: 'info',
            textColor: 'grey-10',
            multiLine: true,
            message: `Se agregó el nuevo registro "${this.nuevo_registro_nombre}"`,
            timeout: 2000
          })
        } catch (error) {
          console.log(error)
        } finally {
          this.nuevo_registro_nombre = undefined
          await this.getRegistros()
        }
      },
      async saveRegistro() {
        try {
          await firebaseDB.collection('Registro').doc(
            this.editar_registro_id).update({nombre: this.editar_registro_nombre})
          this.$q.notify({
            type: 'info',
            textColor: 'grey-10',
            multiLine: true,
            message: `Se modifico el registro "${this.editar_registro_nombre}"`,
            timeout: 2000
          })
        } catch (error) {
          console.log(error)
        } finally {
          this.editar_registro_nombre = undefined
          this.editar_registro_id = undefined
          await this.getRegistros()
        }
      },
      async deleteRegistro() {
        try {
          await firebaseDB.collection('Registro').doc(this.eliminar_registro_id).delete()
          this.$q.notify({
            type: 'negative',
            multiLine: true,
            message: `Se eliminó el registro "${this.eliminar_registro_nombre}"`,
            timeout: 2000
          })
        } catch (error) {
          console.log(error)
        } finally {
          this.eliminar_registro_nombre = undefined
          this.eliminar_registro_id = undefined
          await this.getRegistros()
        }
      },
      cancelar_guardado() {
        this.nuevo_registro_nombre = undefined
        this.editar_registro_nombre = undefined
      },
      editRegistroDialog(props) {
        this.dialogo_editarregistro = true
        this.editar_registro_nombre = props.row.nombre
        this.editar_registro_id = props.row.id
      },
      deleteRegistroDialog(props) {
        this.dialogo_eliminarregistro = true
        this.eliminar_registro_nombre = props.row.nombre
        this.eliminar_registro_id = props.row.id
      },
    }
    ,
    computed: {
      registronuevo_invalido() {
        if (this.nuevo_registro_nombre) {
          let existe = false;
          for (let item of this.datos_registros) {
            if (item.nombre === this.nuevo_registro_nombre) {
              existe = true
            }
          }
          return this.nuevo_registro_nombre.length < 1 || existe
        } else {
          return false
        }
      }
      ,
      registromodificado_invalido() {
        if (this.editar_registro_nombre) {
          let existe = false;
          for (let item of this.datos_registros) {
            if (item.nombre === this.editar_registro_nombre && item.nombre !== this.editar_registro_id) {
              existe = true
            }
          }
          return this.editar_registro_nombre.length < 1 || existe
        } else {
          return false
        }
      }
      ,
      mensaje_error() {
        let mensaje = ""
        for (let item of this.datos_registros) {
          if (item.nombre === this.nuevo_registro_nombre) {
            mensaje += "Ya existe un registro con ese nombre. "
            console.log("existe")
          }
        }
        return mensaje
      }
    }
  }
</script>
