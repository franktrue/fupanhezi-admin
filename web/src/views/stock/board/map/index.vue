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
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="fetchLatest" :loading="loading"><i class="el-icon-refresh" /> 同步数据</el-button>
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
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'boardMap',
  mixins: [d2CrudPlus.crud],
  props: {
    // 容器样式
    boardRow: {
      type: Object,
      required: true
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
    fetchLatest() {
      const that = this
      that.loading = true
      api.FetchData(that.boardRow).then(res => {
        that.$message.success('更新成功')
        that.loading = false
        that.handleSearch()
      })
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      query.code = this.boardRow.code
      return api.GetList(query)
    },
    addRequest (row) {
      row.code = this.boardRow.code
      row.board_name = this.boardRow.name
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
