# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import not_

from nailgun import consts
from nailgun.db import db
from nailgun.db.sqlalchemy.models.base import Base
from nailgun.db.sqlalchemy.models.fields import JSON
from nailgun.db.sqlalchemy.models.node import Role


class Release(Base):
    __tablename__ = 'releases'
    __table_args__ = (
        UniqueConstraint('name', 'version'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    version = Column(String(30), nullable=False)
    can_update_from_versions = Column(JSON, default=[],
                                      nullable=False, server_default='[]')
    description = Column(Unicode)
    operating_system = Column(String(50), nullable=False)
    state = Column(
        Enum(
            *consts.RELEASE_STATES,
            name='release_state'
        ),
        nullable=False,
        default=consts.RELEASE_STATES.unavailable
    )
    networks_metadata = Column(JSON, default=[])
    attributes_metadata = Column(JSON, default={})
    volumes_metadata = Column(JSON, default={})
    modes_metadata = Column(JSON, default={})
    roles_metadata = Column(JSON, default={})
    wizard_metadata = Column(JSON, default={})
    is_deployable = Column(Boolean, default=True, nullable=False)
    deployment_tasks = Column(JSON, default=[])
    vmware_attributes_metadata = Column(JSON, default=[])

    role_list = relationship(
        "Role",
        backref="release",
        cascade="all,delete",
        order_by="Role.id"
    )
    clusters = relationship(
        "Cluster",
        primaryjoin="Release.id==Cluster.release_id",
        backref="release",
        cascade="all,delete"
    )

    #TODO(enchantner): get rid of properties

    @property
    def roles(self):
        return [role.name for role in self.role_list]

    @roles.setter
    def roles(self, new_roles):
        db().query(Role).filter(
            not_(Role.name.in_(new_roles))
        ).filter(
            Role.release_id == self.id
        ).delete(synchronize_session='fetch')

        added_roles = self.roles
        for role in new_roles:
            if role not in added_roles:
                new_role = Role(
                    name=role,
                    release=self
                )
                db().add(new_role)
                added_roles.append(role)

    @property
    def openstack_version(self):
        return self.version.split('-')[0]

    @property
    def fuel_version(self):
        try:
            version = self.version.split('-')[1]
        except IndexError:
            version = ''

        return version

    @property
    def os_weight(self):
        try:
            weight = consts.RELEASE_OS[::-1].index(self.operating_system)
        except ValueError:
            weight = -1

        return weight

    def __cmp__(self, other):
        """Allows to compare two releases

        :other: an instance of nailgun.db.sqlalchemy.models.release.Release
        """
        if self.fuel_version < other.fuel_version:
            return -1
        if self.fuel_version > other.fuel_version:
            return 1

        if self.openstack_version < other.openstack_version:
            return -1
        if self.openstack_version > other.openstack_version:
            return 1

        if self.os_weight == other.os_weight == -1:
            if self.operating_system > other.operating_system:
                return -1
            if self.operating_system < other.operating_system:
                return 1
        else:
            if self.os_weight < other.os_weight:
                return -1
            if self.os_weight > other.os_weight:
                return 1

        return 0
