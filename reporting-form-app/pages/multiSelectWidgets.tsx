import Select, { MultiValue } from 'react-select';
import { WidgetProps } from '@rjsf/utils';

interface OptionType {
  label: string;
  value: string;
}

export default function MultiSelectWidget({
  value = [],
  onChange,
  options,
}: WidgetProps) {
  const allOptions: OptionType[] = options.enumOptions?.map((opt: any) => ({
    label: opt.label,
    value: opt.value,
  })) ?? [];

  const selectedValues = allOptions.filter((opt) =>
    value.includes(opt.value)
  );

  const handleChange = (selected: MultiValue<OptionType>) => {
    onChange(selected.map((opt) => opt.value));
  };

  return (
    <Select
      isMulti
      options={allOptions}
      value={selectedValues}
      onChange={handleChange}
    />
  );
}
