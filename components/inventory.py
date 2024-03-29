import tcod as libtcod

from game_messages import Message
from helper_utils import group_options, group_indexes


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None

    def add_item(self, item):
        results = []

        if (item.item.function_kwargs.get("can_stack")):
            candidates = [x for x in self.items if x.item.function_kwargs.get("can_stack") and x.name == item.name]
            
            if len(candidates) <= 0 and len(self.items) >= self.capacity:
                results.append({
                    'item_added': None,
                    'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
                })
            else:
                results.append({
                    'item_added': item,
                    'message': Message('You pick up {0} {1}(s)!'.format(item.item.function_kwargs["amount"], item.name), libtcod.blue)
                })

                if len(candidates) <= 0:
                    self.items.append(item)
                else:
                    existing = candidates[0]
                    existing.item.function_kwargs["amount"] += item.item.function_kwargs["amount"]

        else:
            if len(self.items) >= self.capacity:
                results.append({
                    'item_added': None,
                    'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
                })
            else:
                results.append({
                    'item_added': item,
                    'message': Message('You pick up the {0}!'.format(item.name), libtcod.blue)
                })

                self.items.append(item)

        return results


    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name), libtcod.yellow)})

        elif item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'targeting': item_entity})

        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    
    def remove_item(self, item):
        self.items.remove(item)


    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name), libtcod.yellow)})

        return results


    def get_options(self):
        options = []
        equip_options = []

        for item in self.items:
            if self.owner and self.owner.equipment and self.owner.equipment.main_hand == item:
                equip_options.append('{0} (on main hand)'.format(item.name))
            elif self.owner and self.owner.equipment and self.owner.equipment.off_hand == item:
                equip_options.append('{0} (on off hand)'.format(item.name))
            elif item.item.function_kwargs.get("can_stack"):
                options.append("{0} {1}(s)".format(item.item.function_kwargs["amount"], item.name))
            else:
                options.append(item.name)

        return equip_options + group_options(options)


    def get_index_from_options(self, option_index):
        return group_indexes(self.get_options())[option_index]