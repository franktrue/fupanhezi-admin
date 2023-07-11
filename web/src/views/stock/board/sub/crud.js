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
        title: '题材名称',
        key: 'name',
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
            { required: true, message: '题材名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入题材名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '题材解析',
        key: 'brief',
        type: 'textarea',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '题材解析必填项' }
          ],
          component: {
            placeholder: '请输入备注',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      // {
      //   title: '成分股',
      //   key: 'cons',
      //   show: false,
      //   type: 'select',
      //   dict: {
      //     url(dict,{form,component}){
      //       return '/api/stock/board/map/dict/?parent_name='+form.parent_name
      //     },
      //     cache: false,
      //     onReady:(data,dict,options)=>{
      //       vm.optionData = data
      //       vm.formOption = options
      //     }
      //   },
      //   form: {
      //     component: {
      //       props: {
      //         separator: ',' ,//多选时，value的分隔符
      //         elProps:{
      //           filterable: true,
      //           multiple: true,
      //           clearable: true,
      //           filterMethod: function(val) {
      //             if(val) {
      //               const arr = []
      //               vm.optionData.forEach((item) => {
      //                 if(val.includes(item.value.substring(0,6))) {
      //                   arr.push(item.value)
      //                 }
      //               })
      //               if (arr.length>0) {
      //                 vm.formOption.form.cons = arr
      //               } else {
      //                 this.$options.parent.dictOptions = vm.optionData.filter((item) => {
      //                   return item.value.includes(val)
      //                 })
      //               }
      //             } else {
      //               this.$options.parent.dictOptions = vm.optionData
      //             }
      //           }
      //         },
      //       }
      //     }
      //   },
      //   valueResolve (row,key) {
      //     if (row.cons !=null && row.cons.length>0) {
      //       const result = row.cons.map(item => {
      //         const [stock_code, stock_name] = item.split(' ');
      //         return { stock_code, stock_name};
      //       });
      //       row.cons = result
      //     }
      //   },
      // },
    ]
  }
}
