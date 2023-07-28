export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      border: false
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      appendToBody: true, // 子表格必须 否则弹出对话框无法显示最顶层
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [
      {
        title: '金额',
        key: 'amount',
        type: 'number',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '金额必填项' }
          ],
          component: {
            name: 'el-input-number',
            props: {
              precision: 2
            }
          },
          scopedSlots: {
            prefix: () => '￥'
          },
        }
      },
      {
        title: '交易ID',
        key: 'transaction_id',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入交易ID'
          }
        }
      },
      {
        title: '状态',
        key: 'status',
        type: 'radio',
        search: {
          disabled: false
        },
        dict:  {
          data: vm.dictionary('withdraw_status')
        },
        form: {
          value: '1',
          rules: [ // 表单校验规则
            { required: true, message: '状态必填项' }
          ],
        },
      },
      {
        title: '渠道类型',
        key: 'type',
        type: 'radio',
        search: {
          disabled: false
        },
        dict:  {
          data: vm.dictionary('withdraw_type')
        },
        form: {
          value: 'person',
          rules: [ // 表单校验规则
            { required: true, message: '类型必填项' }
          ],
        },
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false }
    }))
  }
}
