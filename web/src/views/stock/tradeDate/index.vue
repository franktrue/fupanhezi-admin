<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">交易日</template>
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <!-- 自动绑定参数与事件 -->
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
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData } from './api' // 查询添加修改删除的http请求接口
export default {
  name: 'stockTradeDate',
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    return {
      loading: false
    }
  },
  methods: {
    // 获取最新交易日
    fetchLatest() {
      const that = this
      this.$confirm('是否确认更新?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return FetchData().then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        }).catch(e => {
          that.loading = false
        })
      })
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return GetList(query)
    }, // 数据请求
    addRequest (row) {
      return AddObj(row)
    }, // 添加请求
    updateRequest (row) {
      return UpdateObj(row)
    }, // 修改请求
    delRequest (row) {
      return DelObj(row.id)
    } // 删除请求
  }
}
</script>
