<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">测试页面1</template>-->
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @seatOffice="seatOffice"
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
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="fetchLatest" :loading="loading">
            <i class="el-icon-refresh" /> 同步数据
          </el-button>
          <el-button size="small" type="info" v-permission="'Fetch'" @click="setCache" :loading="loading">
            <i class="el-icon-s-grid" /> 缓存
          </el-button>
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
        <span>关联营业部</span>
        <el-tag size="small" style="margin-left: 10px">{{ subjectRow.name }}</el-tag>
      </div>
    <seat-office style="margin-top: 80px; margin-left: 10px" :subjectRow="subjectRow">
    </seat-office>
    </el-drawer>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import SeatOffice from '@/views/stock/seat/office'
export default {
  name: 'seat',
  components: { SeatOffice },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      loading: false,
      drawer: false,
      subjectRow: {}
    }
  },
  methods: {
    fetchLatest() {
      const that = this
      this.$confirm('是否确认更新?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return api.FetchObj().then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        }).catch(e => {
          that.loading = false
        })
      })
    },
    setCache() {
      const that = this
      this.$confirm('更新缓存?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return api.CacheObj().then(res => {
          that.loading = false
          that.$message.success('操作成功')
        }).catch(e => {
          that.loading = false
        })
      })
    },
    seatOffice (scope) {
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
