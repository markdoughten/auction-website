export interface MetaAttributes {
  [key: string]: number; //_ID
}

export interface MetaSubCategory {
  // _id: number;
  // _attributes: string[];
  [key: string]: MetaAttributes | number | string[];
}

export interface MetaCategory {
  // _id: number;
  // _attributes: string[];
  [key: string]: MetaSubCategory | number | string[];
}

export interface MetaItems {
  [key: string]: MetaCategory | string[];
}

export const _ID: string = "item_meta_id";
export const _ATTR: string = "item_meta_attrs";
