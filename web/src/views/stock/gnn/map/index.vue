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
          <el-button size="small" type="info" v-permission="'Fetch'" @click="batchTranfer"><i class="el-icon-sort" /> 批量转化</el-button>
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
        批量转化 <small>将股票同步到自定义题材</small>
      </template>

      <el-form :model="batchForm" ref="batchForm" :rules="batchFormRules" :inline="true">
        <el-form-item label="概念题材" prop="name">
          <el-select
            v-model="batchForm.name"
            clearable
            filterable
            remote
            reserve-keyword
            placeholder="请输入关键词"
            :remote-method="remoteMethod"
            :loading="loading">
            <el-option
              v-for="item in conceptOptions"
              :key="item.name"
              :label="item.parent_name + '/' + item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData" :loading="loading">确定</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { GetList as GetConceptSub } from '@/views/stock/board/sub/api'
import { BatchData } from '@/views/stock/board/map/api'
let id = 0
export default {
  name: 'boardMap',
  mixins: [d2CrudPlus.crud],
  props: {
    // 容器样式
    subjectRow: {
      type: Object,
      required: true
    }
  },
  watch: {
    subjectRow () {
      this.doRefresh({ from: 'load' })
    }
  },
  data () {
    return {
      loading: false,
      dialogFormVisible: false,
      batchForm: {},
      batchFormRules: {
        name: [
          { required: true, message: '必填项' }
        ],
      },
      conceptOptions:[]
    }
  },
  methods: {
    remoteMethod(query) {
      if (query !== '') {
        this.loading = true;
        GetConceptSub({limit: 999, name: query}).then((res) => {
          this.conceptOptions = res.data.data
          this.loading = false;
        })
      } else {
        this.options = [];
      }
    },
    batchTranfer() {
      const that = this
      if (that.multipleSelection == null || that.multipleSelection.length === 0) {
        that.$message({
          message: '您还未选择数据',
          type: 'warning'
        })
        return
      }
      that.dialogFormVisible = true
    },
    submitData() {
      this.$refs.batchForm.validate((valid) => {
        if (valid) {
          this.loading = true
          const ids = []
          let rowKey = this.crud.options.rowKey
          console.log(rowKey)
          if (this.isVxeTable()) {
            rowKey = this.crud.options.rowId
          }
          for (const row of this.multipleSelection) {
            ids.push(row[rowKey])
          }
          this.batchForm.ids = ids
          BatchData(this.batchForm).then(res => {
            this.$message.success('操作成功')
            this.dialogFormVisible = false
            this.loading = false
          }).catch(e => {
            this.loading = false
          })

        }
      })

    },
    fetchLatest() {
      const that = this
      that.loading = true
      api.FetchData(that.subjectRow).then(res => {
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
      query.code = this.subjectRow.code
      return api.GetList(query)
    },
    addRequest (row) {
      row.code = this.subjectRow.code
      row.name = this.subjectRow.name
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
