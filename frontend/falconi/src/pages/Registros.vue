<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Registros" icon="mdi-file-edit"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getRegistros()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn v-if="es_usuario" style="margin-left: 8px;" color="green" @click="addRegistroDialog()">
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
          :columns="columnas"
          :visible-columns="visible_columnas"
          row-key="id"
          :loading="tabla_loading"
          :filter="filter"
        >
          <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar" style="margin-right: 12px;">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
            <q-select
              v-model="visible_columnas"
              multiple
              outlined
              dense
              options-dense
              :display-value1="$q.lang.table.columnas"
              display-value="Mostrar columnas..."
              emit-value
              map-options
              :options="columnas"
              option-value="name"
              options-cover
              style="min-width: 150px"
            />
          </template>



          <template v-slot:header="props">
            <q-tr :props="props">
              <q-th
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                {{ col.label }}
              </q-th>
              <q-th auto-width/>
            </q-tr>
          </template>

          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td v-for="col in props.cols" :key="col.name" :props="props">{{ col.value }}</q-td>
              <q-td auto-width>
                <q-btn dense round flat color="accent" @click="props.expand = !props.expand"
                       :icon="props.expand ? 'remove' : 'add'"></q-btn>
                <q-btn v-if="es_usuario" dense round flat color="primary" @click="editRegistroDialog(props)"
                       icon="edit"></q-btn>
                <q-btn v-if="es_usuario" dense round flat color="red" @click="deleteRegistroDialog(props)"
                       icon="delete"></q-btn>
              </q-td>
            </q-tr>
            <q-tr v-show="props.expand" :props="props">
              <q-td colspan="100%">
                <div class="text-left">
                  <q-tr>
                    <q-td>Encabezado</q-td>
                    <q-td>
                      <q-tr>
                        <q-td style="height: initial; border-bottom-width: 0;">{{ props.row.encabezado }}</q-td>
                      </q-tr>
                    </q-td>
                  </q-tr>
                  <q-tr>
                    <q-td>Transcripción</q-td>
                    <q-td>
                      <q-tr>
                        <q-td style="height: initial; border-bottom-width: 0;">
                          <pre>{{ props.row.transcripcion }}</pre>
                        </q-td>
                      </q-tr>
                    </q-td>
                  </q-tr>
                  <q-tr>
                    <q-td>Observaciones</q-td>
                    <q-td>
                      <q-tr>
                        <q-td style="height: initial; border-bottom-width: 0;">
                          <pre>{{ props.row.observaciones }}</pre>
                        </q-td>
                      </q-tr>
                    </q-td>
                  </q-tr>
                  <q-tr v-if="es_usuario">
                    <q-td>Notas</q-td>
                    <q-td>
                      <q-tr>
                        <q-td style="height: initial; border-bottom-width: 0;">
                          <pre>{{ props.row.notas }}</pre>
                        </q-td>
                      </q-tr>
                    </q-td>
                  </q-tr>
                </div>
              </q-td>
            </q-tr>
          </template>

        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevoregistro" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="green" text-color="white"/>
          <q-toolbar-title>Agregar nuevo registro</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <div class="row q-pt-md">
            <div class="col">
              <q-select clearable name="archivo" label="Archivo" :options="archivos" v-model="registro_archivo"/>
              <q-select clearable name="fondo" label="Fondo" :options="fondos" v-model="registro_fondo"/>
              <q-select clearable name="tipo_documento" label="Tipo de documento" :options="tipos_documento" v-model="registro_tipodocumento"/>
              <q-input clearable name="libro" label="Libro" v-model="registro_libro" type="number" min="1"/>
              <q-input clearable name="foja" label="Fojas" v-model="registro_foja"/>
              <q-input clearable name="caja" label="Caja" v-model="registro_caja"/>
              <q-input clearable name="expediente" label="Expediente" v-model="registro_expediente"/>
              <q-select clearable name="años" label="Años" v-model="registro_anos" use-input use-chips multiple
                        hide-dropdown-icon input-debounce="0" new-value-mode="add-unique"/>
              <q-select clearable name="lugar" label="Lugar" :options="lugares" v-model="registro_lugar"/>
              <q-select clearable name="ramo" label="Ramo" :options="ramos" v-model="registro_ramo"/>
              <q-input clearable name="encabezado" label="Encabezado y/o resumen" type="textarea" rows="1" autogrow v-model="registro_encabezado"/>
              <q-input clearable name="personas_involucradas" label="Personas involucradas" type="textarea" rows="1" autogrow
                       v-model="registro_personasinvolucradas"/>
              <q-input clearable name="transcripcion" label="Transcripción" type="textarea" rows="1" autogrow
                       v-model="registro_transcripcion"/>
              <q-input clearable name="observaciones" label="Observaciones" type="textarea"
                       rows="1" autogrow v-model="registro_observaciones"/>
              <q-input clearable name="notas" label="Notas" type="textarea" rows="1" autogrow v-model="registro_notas"/>
            </div>
          </div>
        </q-card-section>
        <br/>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="limpiar_campos()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 @click="addRegistro()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="dialogo_editarregistro" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="edit" color="primary" text-color="white"/>
          <q-toolbar-title>Editar registro</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <div class="row q-pt-md">
            <div class="col">
              <q-select clearable name="archivo" label="Archivo" :options="archivos" v-model="registro_archivo"/>
              <q-select clearable name="fondo" label="Fondo" :options="fondos" v-model="registro_fondo"/>
              <q-select clearable name="tipo_documento" label="Tipo de documento" :options="tipos_documento" v-model="registro_tipodocumento"/>
              <q-input clearable name="libro" label="Libro" v-model="registro_libro" type="number" min="1"/>
              <q-input clearable name="foja" label="Fojas" v-model="registro_foja"/>
              <q-input clearable name="caja" label="Caja" v-model="registro_caja"/>
              <q-input clearable name="expediente" label="Expediente" v-model="registro_expediente"/>
              <q-select clearable name="años" label="Años" v-model="registro_anos" use-input use-chips multiple
                        hide-dropdown-icon input-debounce="0" new-value-mode="add-unique"/>
              <q-select clearable name="lugar" label="Lugar" :options="lugares" v-model="registro_lugar"/>
              <q-select clearable name="ramo" label="Ramo" :options="ramos" v-model="registro_ramo"/>
              <q-input clearable name="encabezado" label="Encabezado y/o resumen" type="textarea" rows="1" autogrow v-model="registro_encabezado"/>
              <q-input clearable name="personas_involucradas" label="Personas involucradas" type="textarea" rows="1" autogrow
                       v-model="registro_personasinvolucradas"/>
              <q-input clearable name="transcripcion" label="Transcripción" type="textarea" rows="1" autogrow
                       v-model="registro_transcripcion"/>
              <q-input clearable name="observaciones" label="Observaciones" type="textarea"
                       rows="1" autogrow v-model="registro_observaciones"/>
              <q-input clearable name="notas" label="Notas" type="textarea"
                       rows="1" autogrow v-model="registro_notas"/>
            </div>
          </div>
        </q-card-section>
        <br/>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="limpiar_campos()"/>
          <q-btn flat label="Guardar cambios" color="primary" v-close-popup
                 @click="updateRegistro()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="dialogo_eliminarregistro" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-delete" color="red" text-color="white"/>
          <q-toolbar-title>Eliminar registro</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <div class="row">
            <p style="margin: 0">¿Está seguro de eliminar este registro?</p>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <div class="row">
            <div class="col">
              <q-select v-if="registro_archivo" readonly name="archivo" label="Archivo" :options="archivos"
                        v-model="registro_archivo"/>
              <q-select v-if="registro_fondo" readonly name="fondo" label="Fondo" :options="fondos"
                        v-model="registro_fondo"/>
              <q-select v-if="registro_tipodocumento" readonly name="tipo_documento" label="Tipo de documento" :options="tipos_documento" v-model="registro_tipodocumento"/>
              <q-input v-if="registro_libro" readonly name="libro" label="Libro" v-model="registro_libro" type="number"
                       min="1"/>
              <q-input v-if="registro_foja" readonly name="foja" label="Fojas" v-model="registro_foja"/>
              <q-input v-if="registro_caja" readonly name="caja" label="Caja" v-model="registro_caja"/>
              <q-input v-if="registro_expediente" readonly name="expediente" label="Expediente"
                       v-model="registro_expediente"/>
              <q-select v-if="registro_anos" readonly name="años" label="Años" v-model="registro_anos" use-input
                        use-chips multiple
                        hide-dropdown-icon input-debounce="0" new-value-mode="add-unique"/>
              <q-select v-if="registro_lugar" readonly name="lugar" label="Lugar" :options="lugares"
                        v-model="registro_lugar"/>
              <q-select v-if="registro_ramo" readonly name="ramo" label="Ramo" :options="ramos"
                        v-model="registro_ramo"/>
              <q-input v-if="registro_encabezado" readonly name="encabezado" label="Encabezado y/o resumen"
                       type="textarea" rows="1" autogrow v-model="registro_encabezado"/>
              <q-input v-if="registro_personasinvolucradas" readonly name="personas_involucradas"
                       label="Personas involucradas" type="textarea" rows="1" autogrow
                       v-model="registro_personasinvolucradas"/>
              <q-input v-if="registro_transcripcion" readonly name="transcripcion" label="Transcripción" type="textarea"
                       rows="1" autogrow
                       v-model="registro_transcripcion"/>
              <q-input v-if="registro_observaciones" readonly name="observaciones" label="Observaciones" type="textarea"
                       rows="1" autogrow
                       v-model="registro_observaciones"/>
              <q-input v-if="registro_notas" readonly name="notas" label="Notas" type="textarea"
                       rows="1" autogrow
                       v-model="registro_notas"/>

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
import firebase from "firebase";
import {date} from 'quasar'


export default {
  name: 'Registros',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevoregistro: false,
      dialogo_editarregistro: false,
      dialogo_eliminarregistro: false,
      registro_archivo: undefined,
      registro_fondo: undefined,
      registro_libro: undefined,
      registro_tipodocumento: undefined,
      registro_foja: undefined,
      registro_caja: undefined,
      registro_expediente: undefined,
      registro_anos: undefined,
      registro_lugar: undefined,
      registro_ramo: undefined,
      registro_encabezado: undefined,
      registro_personasinvolucradas: undefined,
      registro_notas: undefined,
      registro_observaciones: undefined,
      registro_transcripcion: undefined,
      registro_usuario: undefined,
      registro_id: undefined,
      columnas: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {name: 'archivo', align: 'left', label: 'Archivo', field: 'archivo', sortable: true},
        {name: 'fondo', align: 'left', label: 'Fondo', field: 'fondo', sortable: true},
        {name: 'tipo_documento', align: 'left', label: 'Tipo de documento', field: 'tipo_documento', sortable: true},
        {name: 'libro', align: 'left', label: 'Libro', field: 'libro', sortable: true},
        {name: 'foja', align: 'left', label: 'Foja', field: 'foja', sortable: true},
        {name: 'caja', align: 'left', label: 'Caja', field: 'caja', sortable: true},
        {name: 'expediente', align: 'left', label: 'Expediente', field: 'expediente', sortable: true},
        {name: 'años', align: 'left', label: 'Años', field: 'años', sortable: true},
        {name: 'lugar', align: 'left', label: 'Lugar', field: 'lugar', sortable: true},
        {name: 'ramo', align: 'left', label: 'Ramo', field: 'ramo', sortable: true},
        {name: 'encabezado', align: 'left', label: 'Encabezado', field: 'encabezado', sortable: true},
        {name: 'personas_involucradas', align: 'left', label: 'Personas involucradas', field: 'personas_involucradas', sortable: true},
        {name: 'transcripcion', align: 'left', label: 'Transcripcion', field: 'transcripcion', sortable: true},
        {name: 'observaciones', align: 'left', label: 'Observaciones', field: 'observaciones', sortable: true},
        {name: 'creacion', align: 'left', label: 'Creación', field: 'creacion', sortable: true},
        {name: 'crea', align: 'left', label: 'Crea', field: 'crea', sortable: true},
        {name: 'actualizacion', align: 'left', label: 'Actualización', field: 'actualizacion', sortable: true},
        {name: 'actualiza', align: 'left', label: 'Actualiza', field: 'actualiza', sortable: true},
      ],
      visible_columnas: ['archivo', 'fondo', 'libro', 'foja', 'años', 'lugar', 'ramo', 'crea'],
      archivos: undefined,
      fondos: undefined,
      lugares: undefined,
      ramos: undefined,
      tipos_documento: undefined,
      datos_registros: [],
      es_usuario: false,
      es_admin: false,
      usuario: "",
      user_displayname: "",
      firebaseRef: firebaseDB.collection('Registro'),
    }
  },
  mounted() {
    this.getRegistros()
  },
  created() {
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      if ((!(snapshot.docs.length === snapshot.docChanges().length) && snapshot.docChanges().length === 1)) {
        snapshot.docChanges().forEach(change => {
          this.getRegistros()
          if (change.type === "added") {
            this.$q.notify({
              type: 'positive',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se agregó el nuevo registro con ID "${change.doc.id}"`,
              timeout: 2000
            })
          } else if (change.type === "removed") {
            this.$q.notify({
              type: 'negative',
              multiLine: true,
              message: `Se eliminó el registro con ID "${change.doc.id}"`,
              timeout: 2000
            })
          } else if (change.type === "modified") {
            this.$q.notify({
              type: 'info',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se modifico el registro con ID "${change.doc.id}"`,
              timeout: 2000
            })
          }
        })
      }
      this.registro_archivo = undefined
      this.registro_fondo = undefined
      this.registro_tipodocumento = undefined
      this.registro_libro = undefined
      this.registro_foja = undefined
      this.registro_caja = undefined
      this.registro_expediente = undefined
      this.registro_anos = undefined
      this.registro_lugar = undefined
      this.registro_ramo = undefined
      this.registro_encabezado = undefined
      this.registro_notas = undefined
      this.registro_observaciones = undefined
      this.registro_transcripcion = undefined
      this.registro_usuario = undefined
      this.registro_id = undefined
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
        this.usuario = user;
        this.user_displayname = user.displayName
        this.columnas.push(
          {name: 'notas', align: 'left', label: 'Notas', field: 'notas', sortable: true}
        )
      } else {
        this.es_usuario = false;
        if (this.columnas[this.columnas.length - 1].name === 'notas') {
          this.columnas.pop()
        }
      }
    });
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
      }).catch(error => {
        console.log(error);
        this.archivos = []
      })
    },
    getTiposDocumento() {
      firebaseDB.collection('Config').doc('form').get().then(resDB => {
        this.tipos_documento = resDB.data().tipo_documento
      }).catch(error => {
        console.log(error)
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
      this.getTiposDocumento()
    },
    getRegistros() {
      this.tabla_loading = true
      this.getCampos()
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
            tipo_documento: res.data().tipo_documento,
            libro: res.data().libro,
            foja: res.data().foja,
            caja: res.data().caja,
            expediente: res.data().expediente,
            años: years,
            lugar: res.data().lugar,
            ramo: res.data().ramo,
            encabezado: res.data().encabezado,
            personas_involucradas: res.data().personas_involucradas,
            notas: res.data().notas,
            transcripcion: res.data().transcripcion,
            crea: res.data().crea,
            creacion: res.data().creacion,
            actualiza: res.data().actualiza,
            actualizacion: res.data().actualizacion,
          };
          this.datos_registros.push(registro);
        });
      }).catch(error => {
        console.log(error);
        this.tabla_loading = false;
      }).finally(() => {
        this.tabla_loading = false
      })
    },
    addRegistro() {
      const data_registro = {}
      if (this.registro_archivo) data_registro['archivo'] = this.registro_archivo
      if (this.registro_fondo) data_registro['fondo'] = this.registro_fondo
      if (this.registro_tipodocumento) data_registro['tipo_documento'] = this.registro_tipodocumento
      if (this.registro_libro) data_registro['libro'] = this.registro_libro
      if (this.registro_foja) data_registro['foja'] = this.registro_foja
      if (this.registro_caja) data_registro['caja'] = this.registro_caja
      if (this.registro_expediente) data_registro['expediente'] = this.registro_expediente
      if (this.registro_anos) data_registro['años'] = this.registro_anos
      if (this.registro_lugar) data_registro['lugar'] = this.registro_lugar
      if (this.registro_ramo) data_registro['ramo'] = this.registro_ramo
      if (this.registro_encabezado) data_registro['encabezado'] = this.registro_encabezado
      if (this.registro_personasinvolucradas) data_registro['personas_involucradas'] = this.registro_personasinvolucradas
      if (this.registro_notas) data_registro['notas'] = this.registro_notas
      if (this.registro_observaciones) data_registro['observaciones'] = this.registro_observaciones
      if (this.registro_transcripcion) data_registro['transcripcion'] = this.registro_transcripcion
      data_registro['crea'] = this.user_displayname
      data_registro['creacion'] = date.formatDate(Date.now(), 'YYYY-MM-DD')
      firebaseDB.collection('Registro').add(data_registro)
    },
    updateRegistro() {
      const data_registro = {}
      if (this.registro_archivo) data_registro['archivo'] = this.registro_archivo
      if (this.registro_fondo) data_registro['fondo'] = this.registro_fondo
      if (this.registro_tipodocumento) data_registro['tipo_documento'] = this.registro_tipodocumento
      if (this.registro_libro) data_registro['libro'] = this.registro_libro
      if (this.registro_foja) data_registro['foja'] = this.registro_foja
      if (this.registro_caja) data_registro['caja'] = this.registro_caja
      if (this.registro_expediente) data_registro['expediente'] = this.registro_expediente
      if (this.registro_anos) data_registro['años'] = this.registro_anos
      if (this.registro_lugar) data_registro['lugar'] = this.registro_lugar
      if (this.registro_ramo) data_registro['ramo'] = this.registro_ramo
      if (this.registro_encabezado) data_registro['encabezado'] = this.registro_encabezado
      if (this.registro_personasinvolucradas) data_registro['personas_involucradas'] = this.registro_personasinvolucradas
      if (this.registro_notas) data_registro['notas'] = this.registro_notas
      if (this.registro_observaciones) data_registro['observaciones'] = this.registro_observaciones
      if (this.registro_transcripcion) data_registro['transcripcion'] = this.registro_transcripcion
      data_registro['actualiza'] = this.user_displayname
      data_registro['actualizacion'] = date.formatDate(Date.now(), 'YYYY-MM-DD')
      firebaseDB.collection('Registro').doc(this.registro_id).update(data_registro)
    },
    deleteRegistro() {
      firebaseDB.collection('Registro').doc(this.eliminar_registro_id).delete()
    },
    limpiar_campos() {
      this.registro_archivo = undefined
      this.registro_fondo = undefined
      this.registro_tipodocumento = undefined
      this.registro_libro = undefined
      this.registro_foja = undefined
      this.registro_caja = undefined
      this.registro_expediente = undefined
      this.registro_anos = undefined
      this.registro_lugar = undefined
      this.registro_ramo = undefined
      this.registro_encabezado = undefined
      this.registro_personasinvolucradas = undefined
      this.registro_notas = undefined
      this.registro_observaciones = undefined
      this.registro_transcripcion = undefined
      this.registro_usuario = undefined
    },
    addRegistroDialog() {
      this.limpiar_campos()
      this.dialogo_nuevoregistro = true
    },
    editRegistroDialog(props) {
      this.limpiar_campos()
      this.dialogo_editarregistro = true
      if (props.row.id) this.registro_id = props.row.id
      if (props.row.archivo) this.registro_archivo = props.row.archivo
      if (props.row.fondo) this.registro_fondo = props.row.fondo
      if (props.row.tipo_documento) this.registro_tipodocumento = props.row.tipo_documento
      if (props.row.libro) this.registro_libro = props.row.libro
      if (props.row.foja) this.registro_foja = props.row.foja
      if (props.row.caja) this.registro_caja = props.row.caja
      if (props.row.expediente) this.registro_expediente = props.row.expediente
      if (props.row.años) this.registro_anos = props.row.años.split(", ")
      if (props.row.lugar) this.registro_lugar = props.row.lugar
      if (props.row.ramo) this.registro_ramo = props.row.ramo
      if (props.row.encabezado) this.registro_encabezado = props.row.encabezado
      if (props.row.personas_involucradas) this.registro_personasinvolucradas = props.row.personas_involucradas
      if (props.row.notas) this.registro_notas = props.row.notas
      if (props.row.observaciones) this.registro_observaciones = props.row.observaciones
      if (props.row.transcripcion) this.registro_transcripcion = props.row.transcripcion
    },
    deleteRegistroDialog(props) {
      this.limpiar_campos()
      this.dialogo_eliminarregistro = true
      if (props.row.id) this.eliminar_registro_id = props.row.id
      if (props.row.archivo) this.registro_archivo = props.row.archivo
      if (props.row.fondo) this.registro_fondo = props.row.fondo
      if (props.row.tipo_documento) this.registro_tipodocumento = props.row.tipo_documento
      if (props.row.libro) this.registro_libro = props.row.libro
      if (props.row.foja) this.registro_foja = props.row.foja
      if (props.row.caja) this.registro_caja = props.row.caja
      if (props.row.expediente) this.registro_expediente = props.row.expediente
      if (props.row.años) this.registro_anos = props.row.años.split(", ")
      if (props.row.lugar) this.registro_lugar = props.row.lugar
      if (props.row.ramo) this.registro_ramo = props.row.ramo
      if (props.row.encabezado) this.registro_encabezado = props.row.encabezado
      if (props.row.personas_involucradas) this.registro_personasinvolucradas = props.row.personas_involucradas
      if (props.row.notas) this.registro_notas = props.row.notas
      if (props.row.observaciones) this.registro_observaciones = props.row.observaciones
      if (props.row.transcripcion) this.registro_transcripcion = props.row.transcripcion
    }
  }
}
</script>
