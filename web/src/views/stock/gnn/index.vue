<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">测试页面1</template>-->
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @subjectCons="subjectCons"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            v-permission="'Create'"
            type="primary"
            @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="fetchData" :loading="loading"><i class="el-icon-refresh" /> 同步数据</el-button>
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
    <el-drawer :visible.sync="drawer" :size="800">
      <div slot="title">
        <span>成分股列表</span>
        <el-tag size="small" style="margin-left: 10px">{{ subjectRow.name }}</el-tag>
      </div>
      <subject-map
        style="margin-top: 80px; margin-left: 10px"
        :subjectRow="subjectRow"
      >
      </subject-map>
    </el-drawer>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import SubjectMap from '@/views/stock/gnn/map'
export default {
  name: 'gnn',
  components: { SubjectMap },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      loading: false,
      drawer: false,
      subjectRow: {}
    }
  },
  methods: {
    fetchData() {
      const that = this
      that.$confirm('该操作较耗时，会异步更新，请勿轻易操作！', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        api.FetchObj().then(res => {
          that.$message.success('更新成功')
          that.loading = false
          that.handleSearch()
        }).catch(e => {
          that.loading = false
        })
      })

    },
    subjectCons (scope) {
      this.drawer = true
      this.subjectRow = scope.row
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      return api.createObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    /**
     * 懒加载
     * @param row
     * @returns {Promise<unknown>}
     */
    loadContentMethod ({ row }) {
      return new Promise(resolve => {
        api.GetList({ parent: row.id }).then(res => {
          resolve(res.data.data)
        })
      })
    }
  }
}
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
