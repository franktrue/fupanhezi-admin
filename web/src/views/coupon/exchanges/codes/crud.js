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
    selectionRow: {
      align: 'center',
      width: 46
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
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    formOptions: {
      appendToBody: true, // 子表格必须 否则弹出对话框无法显示最顶层
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [
      {
        title: '数量',
        key: 'num',
        type: 'number',
        show: false,
        form: {
          value: 1,
          component: {
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '总数量必填' }]
        },
      },
      {
        title: '兑换码',
        key: 'key',
        type: 'input',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        width: 120,
        form: {
          component: {
            show: false
          }
        },
      },
      {
        title: '开始时间',
        key: 'start_time',
        type: 'input',
        form: {
          component: {
            show: false
          }
        },
      },
      {
        title: '结束时间',
        key: 'end_time',
        type: 'input',
        form: {
          component: {
            show: false
          }
        },
      },
      {
        title: '是否核销',
        key: 'status',
        type: 'radio',
        search: {
          disabled: false,
          component: {
            name: 'dict-select',
            props: {
              clearable: true
            }
          }
        },
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '使用者ID',
        key: 'user_id',
        type: 'input',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          component: {
            show: false
          }
        }
      }
    ]
  }
}
