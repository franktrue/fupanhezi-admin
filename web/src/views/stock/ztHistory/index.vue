<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">涨停股历史</template>
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
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="dialogFormVisible = true"><i class="el-icon-refresh" /> 同步数据</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-dialog
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <template slot="title">
        同步数据 <small>会更新替换指定日期的涨停板数据</small>
      </template>
      <el-form :model="fetchForm" ref="fetchForm" :rules="fetchFormRules" :inline="true">
        <el-form-item label="交易日" prop="trade_date">
          <el-date-picker
            v-model="fetchForm.trade_date"
            value-format="yyyy-MM-dd"
            :clearable="false"
            type="date"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="fetchDataSubmit" :loading="loading">确定</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import dayjs from 'dayjs'
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData } from './api' // 查询添加修改删除的http请求接口
export default {
  name: 'stockZtHistory',
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    const today = dayjs().format('YYYY-MM-DD')
    return {
      dialogFormVisible: false,
      loading: false,
      fetchForm: {
        trade_date: today,
      },
      fetchFormRules: {
        trade_date: [
          { required: true, message: '必填项' }
        ]
      }
    }
  },
  methods: {
    fetchDataSubmit() {
      const that = this
      that.$refs.fetchForm.validate((valid) => {
        if (valid) {
          that.loading = true
          FetchData(that.fetchForm).then((res) => {
            that.dialogFormVisible = false
            that.loading = false
            that.$message.success('操作成功')
            that.handleSearch()
          }).catch(e => {
            that.loading = false
          })
        } else {
          that.$message.error('表单校验失败，请检查')
        }
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
