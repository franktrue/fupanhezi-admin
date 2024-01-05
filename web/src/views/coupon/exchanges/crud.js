import moment from "moment"
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: "vxe-table",
      rowKey: true, // 必须设置，true or false
      rowId: "id",
      height: "100%", // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    rowHandle: {
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
      },
      width: 280,
      fixed: 'right',
      custom: [{
        text: '兑换码',
        type: 'success',
        size: 'small',
        icon: 'el-icon-s-promotion',
        emit: 'exchangeCodes'
      }]

    },
    indexRow: false,
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '名称',
        key: 'name',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          rules: [
            { required: true, message: '请输入使用场景名称' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入名称',
          }
        }
      },
      {
        title: '有效期 年',
        key: 'year_num',
        type: 'number',
        width: 100,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '月',
        key: 'month_num',
        type: 'number',
        width: 60,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '日',
        key: 'day_num',
        type: 'number',
        width: 60,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '对应等级',
        key: 'level',
        type: "number",
        form: {
          value: 1,
          component: {
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '对应等级必填' }],
          helper: "用户默认等级为1级"
        }
      },
      {
        title: '有效期类型',
        key: 'expire_type',
        type: 'radio',
        search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
        dict: {
          data: vm.dictionary('expire_type')
        },
        form: {
          value: "countdown",
          component: {
            props: {
              clearable: true
            }
          },
          helper: "范围表示指定时间范围，倒计时表示领取后开始有效期天数",
        }
      },
      {
        title: '倒计时天数',
        key: 'days',
        type: "number",
        show: false,
        form: {
          component: {
            show (context) {
              const { form } = context
              return form.expire_type == "countdown"
            },
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '天数必填' }]
        }
      },
      {
        title: "日期范围",
        key: "daterange",
        sortable: true,
        type: "daterange",
        show: false,
        form: {
          component: {
            show (context) {
              const { form } = context
              return form.expire_type == "range"
            },
            props: {
              "time-arrow-control": false,
              format: "yyyy-MM-dd",
              valueFormat: "yyyy-MM-dd",
            },
          },
          rules: [{ required: true, message: '天数必填' }]
        },
        valueBuilder(row, key) {
          if (row.expire_type == "range") {
            row.daterange = [
              row.start_time,
              row.end_time,
            ];
          } else {
            row.daterange = [
              moment().format('YYYY-MM-DD'),
              moment().add(1, 'years').format('YYYY-MM-DD'),
            ];
          }
        },
        valueResolve(row, key) {
          console.log(row)
          if (row.daterange != null && row.daterange.length > 1) {
            row.start_time = row.daterange[0];
            row.end_time = row.daterange[1];
          } else {
            row.start_time = moment().format('YYYY-MM-DD');
            row.end_time = moment().add(1, 'years').format('YYYY-MM-DD');
          }
        },
      },
      {
        title: '是否下架',
        key: 'del_flag',
        type: 'dict-switch',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: 0,
          component: {
            props: {
              clearable: true
            }
          },
          helper: "下架后不可用"
        }
      },
      {
        title: '已使用',
        key: 'used_count',
        type: "number",
        form: {
          component: {
            show: false
          }
        }
      }
    ].concat(vm.commonEndColumns())
  }
}
