from torch.utils.data import Dataset, DataLoader


class ComplexUtteranceCodeDataset(Dataset):
  def __init__(
      self, 
      tokenizer, 
      data,
      input_prefix,
      input_label,
      target_label,
      max_input_length,
      max_target_length,
  ):
    self.tokenizer = tokenizer
    self.data = data
    self.max_input_length = max_input_length
    self.max_target_length = max_target_length
    self.input_label = input_label
    self.target_label = target_label
    self.input_prefix = input_prefix

  def __len__(self):
    return len(self.data)

  def __getitem__(self, index : int):
    data_row = self.data.iloc[index]

    input = self.input_prefix + data_row[self.input_label]
    input_encoding = self.tokenizer(
        input,
        max_length = self.max_input_length,
        padding = "max_length",
        truncation=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors="pt"
    )

    target = data_row[self.target_label]
    target_encoding = self.tokenizer(
        target,
        max_length = self.max_target_length,
        padding = "max_length",
        truncation=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors="pt"
    )

    labels = target_encoding["input_ids"]
    labels[labels == 0] = -100

    item = dict(
        input_ids=input_encoding["input_ids"].flatten(),
        attention_mask=input_encoding["attention_mask"].flatten(),
        labels=labels.flatten(),
    )

    item[self.input_label] = input
    item[self.target_label] = target

    extra_columns = [c for c in data_row.keys() if c not in [self.input_label, self.target_label]]
    for column in extra_columns:
      item[column] = data_row[column]

    return item