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
          <div class="row">
            <div class="col">
              <q-select clearable name="archivo" label="Archivo" :options="archivos" v-model="nuevo_registro_archivo" />
              <q-select clearable name="fondo" label="Fondo" :options="fondos" v-model="nuevo_registro_fondo" />
              <q-input clearable name="libro" label="Libro" v-model="nuevo_registro_libro" type="number" min="1" />
              <q-input clearable name="foja" label="Foja" v-model="nuevo_registro_foja" />
              <q-input clearable name="caja" label="Caja" v-model="nuevo_registro_caja" />
              <q-input clearable name="expediente" label="Expediente" v-model="nuevo_registro_expediente" />
              <q-select clearable name="años" label="Años" v-model="nuevo_registro_anos" use-input use-chips multiple hide-dropdown-icon input-debounce="0" new-value-mode="add-unique" />
              <q-select clearable name="lugar" label="Lugar" :options="lugares" v-model="nuevo_registro_lugar" />
              <q-select clearable name="ramo" label="Ramo" :options="ramos" v-model="nuevo_registro_ramo" />
              <q-select clearable name="encabezados" label="Encabezados" v-model="nuevo_registro_encabezados" use-input use-chips multiple hide-dropdown-icon input-debounce="0" new-value-mode="add-unique" />
              <q-select clearable name="notas" label="Notas" v-model="nuevo_registro_notas" use-input use-chips multiple hide-dropdown-icon input-debounce="0" new-value-mode="add-unique" />
              <q-input clearable name="transcripcion" label="Transcripción" type="textarea" rows="1" autogrow v-model="nuevo_registro_transcripcion" />
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="limpiar_campos()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
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
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="limpiar_campos()"/>
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
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="limpiar_campos()"/>
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
      nuevo_registro_archivo: undefined,
      nuevo_registro_fondo: undefined,
      nuevo_registro_libro: undefined,
      nuevo_registro_foja: undefined,
      nuevo_registro_caja: undefined,
      nuevo_registro_expediente: undefined,
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
        {name: 'caja', align: 'left', label: 'Caja', field: 'caja', sortable: true},
        {name: 'expediente', align: 'left', label: 'Expediente', field: 'expediente', sortable: true},
        {name: 'años', align: 'left', label: 'Años', field: 'años', sortable: true},
        {name: 'lugar', align: 'left', label: 'Lugar', field: 'lugar', sortable: true},
        {name: 'ramo', align: 'left', label: 'Ramo', field: 'ramo', sortable: true},
        {name: 'encabezados', align: 'left', label: 'Encabezados', field: 'encabezados', sortable: true},
        {name: 'notas', align: 'left', label: 'Notas', field: 'notas', sortable: true},
        {name: 'transcripcion', align: 'left', label: 'Transcripción', field: 'transcripcion', sortable: true},
        {name: 'usuario', align: 'left', label: 'Usuario', field: 'usuario', sortable: true},

        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      archivos: undefined,
      fondos: undefined,
      lugares: undefined,
      ramos: undefined,
      datos_registros: [],
      noti: () => {
      },
    }
  },
  mounted() {
    this.getCampos()
    this.getRegistros()
  },
  methods: {
    getArchivos() {
      firebaseDB.collection('Archivo').get().then(resDB => {
        let datos_archivos = [];
        resDB.forEach(res => {
          const archivo = res.data().nombre
          datos_archivos.push(archivo)
        });
        this.archivos = datos_archivos
        console.log("datos_archivos: ", datos_archivos);
      }).catch(error => {
        console.log(error);
        this.archivos = []
      })
    },
    getFondos() {
      firebaseDB.collection('Fondo').get().then(resDB => {
        let datos_fondos = [];
        resDB.forEach(res => {
          const fondo = res.data().nombre
          datos_fondos.push(fondo)
        });
        this.fondos = datos_fondos
        console.log("datos_fondos: ", datos_fondos);
      }).catch(error => {
        console.log(error);
        this.fondos = []
      })
    },
    getLugares() {
      firebaseDB.collection('Lugar').get().then(resDB => {
        let datos_lugares = [];
        resDB.forEach(res => {
          const lugar = res.data().nombre
          datos_lugares.push(lugar)
        });
        this.lugares = datos_lugares
        console.log("datos_lugares: ", datos_lugares);
      }).catch(error => {
        console.log(error);
        this.lugares = []
      })
    },
    getRamos() {
      firebaseDB.collection('Ramo').get().then(resDB => {
        let datos_ramos = [];
        resDB.forEach(res => {
          const lugar = res.data().nombre
          datos_ramos.push(lugar)
        });
        this.ramos = datos_ramos
        console.log("datos_ramos: ", datos_ramos);
      }).catch(error => {
        console.log(error);
        this.ramos = []
      })
    },
    getCampos() {
      this.getArchivos()
      this.getFondos()
      this.getLugares()
      this.getRamos()
    },
    getRegistros() {
      firebaseDB.collection('Registro').get().then(resDB => {
        this.datos_registros = [];
        resDB.forEach(res => {
          let years = "";
          if (res.data().años) {
            years = res.data().años.join(", ")
          }
          const registro = {
            id: res.id,
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
        const data_registros = {}
        if (this.nuevo_registro_archivo) data_registros['archivo'] = this.nuevo_registro_archivo
        if (this.nuevo_registro_fondo) data_registros['fondo'] = this.nuevo_registro_fondo
        if (this.nuevo_registro_libro) data_registros['libro'] = this.nuevo_registro_libro
        if (this.nuevo_registro_foja) data_registros['foja'] = this.nuevo_registro_foja
        if (this.nuevo_registro_caja) data_registros['caja'] = this.nuevo_registro_caja
        const resDB = await firebaseDB.collection('Registro').add(data_registros)
        console.log(resDB.id)
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se agregó el nuevo registro`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.limpiar_campos()
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
    limpiar_campos() {
      this.nuevo_registro_archivo = undefined
      this.nuevo_registro_fondo = undefined
      this.nuevo_registro_libro = undefined
      this.nuevo_registro_foja = undefined
      this.nuevo_registro_caja = undefined
      this.nuevo_registro_expediente = undefined
      this.nuevo_registro_anos = undefined
      this.nuevo_registro_lugar = undefined
      this.nuevo_registro_ramo = undefined
      this.nuevo_registro_encabezados = undefined
      this.nuevo_registro_notas = undefined
      this.nuevo_registro_transcripcion = undefined
      this.nuevo_registro_usuario = undefined
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
    filterFn(val, update, abort) {
      update(() => {
        console.log(val)
        console.log(update)
        const needle = val.toLowerCase()
        console.log(needle)
        this.options = this.total_options.filter(v => v.label.toLowerCase().indexOf(needle) > -1)
      })
    },
  },
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
    },
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
    },
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
  },
  watch: {
    nuevo_registro_anos() {
      console.log(this.nuevo_registro_anos)
    }
  }
}
</script>
