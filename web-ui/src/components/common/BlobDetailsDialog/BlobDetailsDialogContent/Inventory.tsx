import { useTranslation } from 'react-i18next';
import { ItemDto, ItemType } from '../../../../../generated';
import { Box, Typography } from '@mui/material';
import DynamicTooltip from '../../DynamicTooltip';
import Cookie from '@mui/icons-material/Cookie';
import BatteryChargingFull from '@mui/icons-material/BatteryChargingFull';
import CleaningServices from '@mui/icons-material/CleaningServices';
import Extension from '@mui/icons-material/Extension';
import ChargingStation from '@mui/icons-material/ChargingStation';
import Memory from '@mui/icons-material/Memory';
import SdCard from '@mui/icons-material/SdCard';
import Speed from '@mui/icons-material/Speed';
import HomeRepairService from '@mui/icons-material/HomeRepairService';

const inventoryIconMap: Record<ItemType, React.ElementType> = {
  COOKIE: Cookie,
  ENERGY_CELL: BatteryChargingFull,
  CACHE_CLEANER: CleaningServices,
  CACHE: Extension,
  POWER_BANK: ChargingStation,
  PROCESSOR_PASTE: Memory,
  EXTERNAL_STORAGE: SdCard,
  OVERCLOCKING_DEVICE: Speed,
  REPAIR_KIT: HomeRepairService,
  MAINTENANCE_KIT: 'symbol',
  COIN: 'symbol',
  BAG_OF_MONEY: 'symbol',
  SACK_OF_MONEY: 'symbol',
  TREASURE_CHEST: 'symbol',
};

const INFINITE_DURABILITY = -1;

const UNCONSUMABLE_ITEM_TYPES: ItemType[] = [
  ItemType.Cache,
  ItemType.PowerBank,
  ItemType.ProcessorPaste,
  ItemType.OverclockingDevice,
  ItemType.ExternalStorage,
];

const isUnconsumable = (type: ItemType) => UNCONSUMABLE_ITEM_TYPES.includes(type);
const hasChargeCount = (item: ItemDto) => isUnconsumable(item.type) && item.durability !== INFINITE_DURABILITY;
const isDepleted = (item: ItemDto) => isUnconsumable(item.type) && item.durability === 0;

const getDepletedIconColor = (type: ItemType) =>
  type === ItemType.OverclockingDevice ? 'error.main' : 'text.disabled';

const getChargeCountKey = (durability: number) => {
  if (durability === 0) {
    return 'blob_details.inventory_no_charge';
  }
  if (durability === 1) {
    return 'blob_details.inventory_single_charge';
  }
  return 'blob_details.inventory_multiple_charges';
};

const Inventory = ({ inventory }: { inventory: ItemDto[] }) => {
  const { t } = useTranslation();

  const getItemLabel = (item: ItemDto) => {
    const name = t(`blob_details.inventory_items.${item.type}`);
    return hasChargeCount(item) ? `${name}${t(getChargeCountKey(item.durability), { count: item.durability })}` : name;
  };

  return (
    <Box display="flex" flexDirection="row" gap={0.5}>
      <Typography variant="body1">
        <strong>{t('blob_details.inventory')}:</strong>
      </Typography>
      <Box display="flex" flexWrap="wrap" gap={1}>
        {inventory.map((item) => {
          const Icon = inventoryIconMap[item.type];
          if (!Icon) {
            return null;
          }

          return (
            <DynamicTooltip key={item.type} title={getItemLabel(item)} placement="top">
              <Box display="inline-flex" alignItems="center" justifyContent="center" sx={{ cursor: 'pointer' }}>
                <Icon fontSize="small" sx={isDepleted(item) ? { color: getDepletedIconColor(item.type) } : undefined} />
              </Box>
            </DynamicTooltip>
          );
        })}
      </Box>
    </Box>
  );
};

export default Inventory;
