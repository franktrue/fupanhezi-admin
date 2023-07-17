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
        title: '平台',
        key: 'auth_type',
        width: 100,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '来源平台必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入来源平台'
          }
        }
      },
      {
        title: '平台Key',
        key: 'auth_key',
        width: 100,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '平台Key必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入平台Key'
          },
        },
      },
    ]
  }
}
