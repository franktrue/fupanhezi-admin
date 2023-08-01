<template>
  <d2-container>
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { request } from '@/api/service'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'

export default {
  name: 'boardSub',
  mixins: [d2CrudPlus.crud],
  props: {
    // 容器样式
    boardRow: {
      type: Object,
      required: true
    },
    option: {
      type: Array,
      required: false
    }
  },
  watch: {
    boardRow () {
      this.doRefresh({ from: 'load' })
    }
  },
  data () {
    return {
      loading: false
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      query.parent_name = this.boardRow.name
      query.type = this.boardRow.type
      return api.GetList(query)
    },
    addRequest (row) {
      row.parent_name = this.boardRow.name
      row.type = this.boardRow.type
      return api.createObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    doAfterRowChange (row) {
      this.doRefresh({ from: 'afterRowChange' })
    },
    doDialogOpened(context) {
      context.form.parent_name = this.boardRow.name
      context.form.type = this.boardRow.type
      if (context.form.name) {
        request({
          url: '/api/stock/board/map/dict/',
          method: 'get',
          params: {name: context.form.name, type: "sub_concept"}
        }).then(res => {
          context.form.cons = res.data.map(item => {
            return item['value']
          })
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
