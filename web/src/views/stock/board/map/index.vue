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
          <el-button size="small" type="success" @click="addBatch"
            ><i class="el-icon-plus" /> 批量新增</el-button
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
    <el-dialog
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      :append-to-body="true"
      width="40%"
    >
      <template slot="title">
        批量新增
      </template>

      <el-form :model="batchForm" ref="batchForm" :inline="true">
        <el-form-item label="股票代码" prop="stocks">
          <el-select
            v-model="batchForm.stocks"
            multiple
            filterable
            remote
            reserve-keyword
            placeholder="请输入关键词"
            :remote-method="remoteStocks"
            :loading="loading">
            <el-option
              v-for="item in stockOptions"
              :key="item.stock_code"
              :label="item.stock_code + item.stock_name"
              :value="item.stock_code + '/' + item.stock_name">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="batchSubmit" :loading="loading">确定</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api'
import { SearchStocks } from '@/views/stock/histrory/api'
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
      loading: false,
      dialogFormVisible: false,
      batchForm: {
        stocks: []
      },
      stockOptions:[]
    }
  },
  methods: {
    addBatch() {
      this.dialogFormVisible = true
      this.batchForm.stocks = []
    },
    remoteStocks(query) {
      SearchStocks({query: query}).then(res => {
        this.stockOptions = res.data
      })
      console.log(this.stockOptions)
    },
    batchSubmit() {
      api.BatchData({
        code: this.boardRow.code,
        board_name: this.boardRow.name,
        type: this.boardRow.type,
        stocks: this.batchForm.stocks
      }).then(res => {
        this.$message.success('更新成功')
        this.loading = false
        this.dialogFormVisible = false
        this.handleSearch()
      }).catch(e => {
        this.loading = false
      })
    },
    fetchLatest() {
      const that = this
      that.loading = true
      api.FetchData(that.boardRow).then(res => {
        that.$message.success('更新成功')
        that.loading = false
        that.handleSearch()
      }).catch(e => {
        that.loading = false
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
